# vim: set fileencoding=utf-8 :
from unittest import TestCase

import gevent
from gevent_zeromq import zmq
from mock import MagicMock

from madacraserver.messaging import (
        MessageHub,
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
        receiver = hub.get_receiver(topics=["A", ], start=True)

        hub.send_message("A", {"a": 1})
        self.assertEqual(receiver.get_message(timeout=10), ("A", {"a": 1}))

        hub.kill(block=True, timeout=10)
        receiver.kill(block=True, timeout=10)

    def test_subscriptions(self):
        hub = MessageHub(context=self.context)
        hub.start()
        receiver = hub.get_receiver(topics=["A", ], start=True)
        receiver.subscribe("B")

        hub.send_message("B", {"b": 1})
        hub.send_message("C", {"c": 1})
        hub.send_message("A", {"a": 1})
        self.assertEqual(receiver.get_message(timeout=10), ("B", {"b": 1}))
        self.assertEqual(receiver.get_message(timeout=10), ("A", {"a": 1}))

        receiver.kill(block=True, timeout=10)
        hub.kill(block=True, timeout=10)

    def test_reactor(self):
        hub = MessageHub(context=self.context)
        hub.start()
        reactor = MessageReactor(hub.get_receiver())
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
