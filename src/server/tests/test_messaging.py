# vim: set fileencoding=utf-8 :
from unittest import TestCase

import gevent
from gevent_zeromq import zmq
from mock import MagicMock

from madacraserver.utils.messaging import (
        MessageHub,
        MessageQueue,
        MessageReactor,
        )


class MessagingTest(TestCase):
    zeromq = 1

    def setUp(self):
        self.context = zmq.Context()
        self.addCleanup(self.context.destroy)

    def test_messaging(self):
        hub = MessageHub(context=self.context)
        hub.start()
        queue = MessageQueue.from_hub(hub, topics=["A", ])
        queue.start()

        hub.send_message("A", {"a": 1})
        self.assertEqual(queue.get_message(timeout=10), ("A", {"a": 1}))

        queue.kill(block=True, timeout=10)
        hub.kill(block=True, timeout=10)

    def test_subscriptions(self):
        hub = MessageHub(context=self.context)
        hub.start()
        queue = MessageQueue.from_hub(hub, topics=["A", ])
        queue.start()
        queue.subscribe("B")

        hub.send_message("B", {"b": 1})
        hub.send_message("C", {"c": 1})
        hub.send_message("A", {"a": 1})
        self.assertEqual(queue.get_message(timeout=10), ("B", {"b": 1}))
        self.assertEqual(queue.get_message(timeout=10), ("A", {"a": 1}))

        queue.kill(block=True, timeout=10)
        hub.kill(block=True, timeout=10)

    def test_reactor(self):
        hub = MessageHub(context=self.context)
        hub.start()
        reactor = MessageReactor.from_hub(hub)
        reactor.start()

        callback = MagicMock()
        reactor.register_callback("A", callback)

        hub.send_message("B", {})
        data = {"a": 1}
        hub.send_message("A", data)

        gevent.sleep(1.0)
        callback.assert_called_once_with("A", data)

        reactor.kill(block=True, timeout=10)
        hub.kill(block=True, timeout=10)
