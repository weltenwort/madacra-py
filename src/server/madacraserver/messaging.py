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
    def __init__(self, socket_address="inproc://messages", context=None):
        super(MessageHub, self).__init__()
        self.socket_address = socket_address
        self.context = context or zmq.Context.instance()
        self.sender = MessageSender(
                socket_address=self.socket_address,
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

    def get_receiver(self, topics=(), start=False):
        receiver = MessageReceiver(
                socket_address=self.socket_address,
                topics=topics,
                context=self.context,
                )
        if start:
            receiver.start()
        return receiver


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
        self.message_queue = Queue()
        self.socket = self.context.socket(zmq.SUB)

        for topic in self.topics:
            self.subscribe(topic)

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
                    self.message_queue.put((topic, message))
                except gevent.GreenletExit:
                    break
                except KeyboardInterrupt:
                    break
                except:
                    logging.exception("Receiving failed.")
        finally:
            self.socket.close()

    def subscribe(self, topic):
        self.topics.add(topic)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

    def get_message(self, block=True, timeout=None, default=None):
        try:
            return self.message_queue.get(block=block, timeout=timeout)
        except Empty:
            return default


class MessageReactor(Greenlet):
    def __init__(self, receiver, start_receiver=True):
        super(MessageReactor, self).__init__()
        self.receiver = receiver
        self.start_receiver = start_receiver
        self.callbacks = collections.defaultdict(list)

    def _run(self):
        if self.start_receiver:
            self.receiver.start()

        try:
            for topic, message in self.receiver.message_queue:
                if topic in self.callbacks:
                    for callback in self.callbacks[topic]:
                        callback(topic, message)
        finally:
            if self.start_receiver:
                self.receiver.kill()

    def register_callback(self, topics, callback):
        if isinstance(topics, basestring):
            topics = [topics, ]

        for topic in topics:
            self.receiver.subscribe(topic)
            self.callbacks[topic].append(callback)

        return callback
