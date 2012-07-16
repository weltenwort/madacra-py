# vim: set fileencoding=utf-8 :
from unittest import TestCase

from gevent_zeromq import zmq

from madacraserver.messaging import (
        MessageHub,
        )


class MessagingTest(TestCase):
    zeromq = 1

    def setUp(self):
        self.context = zmq.Context()
        self.addCleanup(self.context.term)

    def test_messaging(self):
        hub = MessageHub(context=self.context)
        hub.start()
        receiver = hub.get_receiver(topics=["A", ])

        hub.send_message("A", {"a": 1})
        self.assertEqual(receiver.get_message(timeout=10), ("A", {"a": 1}))

        hub.kill(block=True, timeout=10)
        receiver.kill(block=True, timeout=10)

    def test_subscriptions(self):
        hub = MessageHub(context=self.context)
        hub.start()
        receiver = hub.get_receiver(topics=["A", ])
        receiver.subscribe("B")

        hub.send_message("B", {"b": 1})
        hub.send_message("C", {"c": 1})
        hub.send_message("A", {"a": 1})
        self.assertEqual(receiver.get_message(timeout=10), ("B", {"b": 1}))
        self.assertEqual(receiver.get_message(timeout=10), ("A", {"a": 1}))

        receiver.kill(block=True, timeout=10)
        hub.kill(block=True, timeout=10)
