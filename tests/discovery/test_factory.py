from unittest import TestCase

from dredd.discovery.factory import Factory
from dredd.discovery.eureka import Eureka


class FactoryTest(TestCase):
    def test_returns_valid_instances(self):
        factory = Factory()
        eureka = factory.get_discovery('eureka', 'some-url')

        assert isinstance(eureka, Eureka)

    def test_that_it_fails_when_asking_not_implemented_discovery(self):
        factory = Factory()
        self.assertRaises(NotImplementedError,
                          factory.get_discovery, 'not-implemented', 'some-url')
