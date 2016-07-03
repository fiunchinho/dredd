from unittest import TestCase

from dredd.cloud.factory import Factory
from dredd.cloud.aws import Aws
from dredd.cloud.noop import NoOp


class FactoryTest(TestCase):
    def test_returns_valid_instances(self):
        factory = Factory()

        assert isinstance(factory.get_cloud('aws', 'eu-west-1'), Aws)
        assert isinstance(factory.get_cloud('dry-run', 'anything'), NoOp)

    def test_that_it_fails_when_asking_not_implemented_cloud(self):
        factory = Factory()
        self.assertRaises(NotImplementedError,
                          factory.get_cloud, 'not-implemented', 'whatever')
