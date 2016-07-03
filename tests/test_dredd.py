from unittest import TestCase

from mock import Mock

from dredd.discovery.fakediscovery import FakeDiscovery
from dredd.dredd import Dredd, Suspect
from dredd.instance import Instance


class DreddTest(TestCase):
    def test_mark_unhealthy_as_suspicious(self):
        discovery = FakeDiscovery()
        discovery.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery.add(Instance("xyz", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances = discovery.instances()
        dredd = Dredd()
        dredd.patrol(instances)
        # assert dredd.getsuspects() == [Suspect(instances[1], 1)]
        assert dredd.getsuspects()[0].instance.id == instances[1].id

    def test_remove_healthy_from_suspects(self):
        dredd = Dredd()

        discovery = FakeDiscovery()
        discovery.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery.add(Instance("xyz", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances_1 = discovery.instances()

        dredd.patrol(instances_1)

        discovery2 = FakeDiscovery()
        discovery2.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery2.add(Instance("xyz", "name", "dns", "asg", "healthy"))
        discovery2.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances_2 = discovery2.instances()

        dredd.patrol(instances_2)
        self.assertFalse(dredd.getsuspects())

    def test_count_suspects_failures(self):
        dredd = Dredd()

        discovery = FakeDiscovery()
        discovery.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery.add(Instance("xyz", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("opq", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances = discovery.instances()

        dredd.patrol(instances)
        assert dredd.getsuspects()[0].failures == 1
        dredd.patrol(instances)
        assert dredd.getsuspects()[0].failures == 2

    def test_punish_suspects_with_too_many_failures(self):
        dredd = Dredd()
        dredd.punish = Mock()

        discovery = FakeDiscovery()
        discovery.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery.add(Instance("xyz", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("opq", "name", "dns", "asg", "unhealthy"))
        discovery.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances_1 = discovery.instances()

        discovery2 = FakeDiscovery()
        discovery2.add(Instance("abc", "name", "dns", "asg", "healthy"))
        discovery2.add(Instance("xyz", "name", "dns", "asg", "unhealthy"))
        discovery2.add(Instance("opq", "name", "dns", "asg", "healthy"))
        discovery2.add(Instance("def", "name", "dns", "asg", "healthy"))
        instances_2 = discovery2.instances()

        dredd.patrol(instances_1)
        dredd.patrol(instances_1)
        dredd.patrol(instances_2)

        dredd.punish.assert_called_with(instances_1[1])
