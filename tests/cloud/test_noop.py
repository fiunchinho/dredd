from unittest import TestCase

from dredd.cloud.noop import NoOp


class NoOpTest(TestCase):
    def test_noop_does_not_do_anything(self):
        noop = NoOp()
        noop.terminate('any-id')
