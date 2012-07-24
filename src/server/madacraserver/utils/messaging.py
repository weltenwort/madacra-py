# vim: set fileencoding=utf-8 :
import collections
import json
import logging

import gevent
from gevent import Greenlet
from gevent.queue import Queue, Empty
from gevent_zeromq import zmq


class JsonSerializer(object):
    def serialize(self, obj):
        return json.dumps(obj)

    def deserialize(self, data):
        return json.loads(data)


class MessageHub(Greenlet):
    def __init__(self, socket_address="inproc://messages", serializer=None, context=None):
        super(MessageHub, self).__init__()
        self.socket_address = socket_address
        self.serializer = serializer or JsonSerializer()
        self.context = context or zmq.Context.instance()
        self.sender = MessageSender(
                socket_address=self.socket_address,
                serializer=self.serializer,
                context=self.context,
                )

    def _run(self):
        try:
            self.sender.start()
            self.sender.join()
        finally:
            self.sender.kill(block=True, timeout=10.0)

    def send_message(self, topic, message):
        self.sender.queue_message(topic, message)


class MessageSender(Greenlet):
    def __init__(self, socket_address, serializer=None, context=None):
        super(MessageSender, self).__init__()
        self.socket_address = socket_address
        self.serializer = serializer or JsonSerializer()
        self.context = context or zmq.Context.instance()
        self.message_queue = Queue()
        self.socket = self.context.socket(zmq.PUB)

    def _run(self):
        self.socket.bind(self.socket_address)
        gevent.sleep(0.5)

        try:
            for topic, message in self.message_queue:
                try:
                    serialized_message = self.serializer.serialize(message)
                    self.socket.send_multipart((topic, serialized_message))
                except gevent.GreenletExit:
                    break
                except KeyboardInterrupt:
                    break
                except:
                    logging.exception("Sending with topic '{}' failed.".format(topic))
        finally:
            self.socket.close()

    def queue_message(self, topic, message):
        self.message_queue.put((topic, message))


class MessageReceiver(Greenlet):
    def __init__(self, socket_address, topics=(), serializer=None, context=None):
        super(MessageReceiver, self).__init__()
        self.socket_address = socket_address
        self.topics = set(topics)
        self.serializer = serializer or JsonSerializer()
        self.context = context or zmq.Context.instance()
        self.socket = self.context.socket(zmq.SUB)

        for topic in self.topics:
            self.subscribe(topic)

    @classmethod
    def from_hub(cls, message_hub, topics=(), **kwargs):
        return cls(
                socket_address=message_hub.socket_address,
                topics=topics,
                serializer=message_hub.serializer,
                context=message_hub.context,
                **kwargs
                )

    def _run(self):
        while True:
            try:
                self.socket.connect(self.socket_address)
            except zmq.ZMQError:
                gevent.sleep(0.1)
            else:
                break

        try:
            while True:
                try:
                    topic, serialized_message = self.socket.recv_multipart()
                    message = self.serializer.deserialize(serialized_message)
                    self._process_message(topic, message)
                except gevent.GreenletExit:
                    break
                except KeyboardInterrupt:
                    break
                except:
                    logging.exception("Receiving failed.")
        finally:
            self.socket.close()

    def _process_message(self, topic, message):
        """Processes a message. Override in subclasses."""
        pass

    def subscribe(self, topic):
        self.topics.add(topic)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)


class MessageQueue(MessageReceiver):
    def __init__(self, *args, **kwargs):
        super(MessageQueue, self).__init__(*args, **kwargs)
        self.message_queue = Queue()

    def _process_message(self, topic, message):
        self.message_queue.put((topic, message))

    def get_message(self, block=True, timeout=None, default=None):
        try:
            return self.message_queue.get(block=block, timeout=timeout)
        except Empty:
            return default


class MessageReactor(MessageReceiver):
    def __init__(self, *args, **kwargs):
        super(MessageReactor, self).__init__(*args, **kwargs)
        self.callbacks = collections.defaultdict(list)

    def _process_message(self, topic, message):
        if topic in self.callbacks:
            for callback in self.callbacks[topic]:
                callback(topic, message)

    def register_callback(self, topics, callback):
        if isinstance(topics, basestring):
            topics = [topics, ]

        for topic in topics:
            self.subscribe(topic)
            self.callbacks[topic].append(callback)

        return callback


class MessageDebugLogger(MessageReceiver):
    def __init__(self, *args, **kwargs):
        if "logger" in kwargs:
            self.logger = kwargs["logger"]
            del kwargs["logger"]
        else:
            self.logger = logging.getLogger()
        super(MessageDebugLogger, self).__init__(*args, **kwargs)
        self.subscribe("")

    def _process_message(self, topic, message):
        self.logger.debug("[{}] {}".format(topic, message))
