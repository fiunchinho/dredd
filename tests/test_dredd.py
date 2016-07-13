from unittest import TestCase

from mock import Mock

from dredd.dredd import Dredd, Suspect
from dredd.instance import Instance


class DreddTest(TestCase):
    def test_mark_unhealthy_as_suspicious(self):
        instances = [Instance("abc", "name", "address", Instance.STATUS_UP),
                     Instance("xyz", "name", "address", Instance.STATUS_DOWN),
                     Instance("def", "name", "address", Instance.STATUS_UP)]

        dredd = Dredd()
        dredd.patrol(instances)
        # assert dredd.getsuspects() == [Suspect(instances[1], 1)]
        assert dredd.getsuspects()[0].instance.id == instances[1].id

    def test_remove_healthy_from_suspects(self):
        dredd = Dredd()

        instances_1 = [Instance("abc", "name", "address", Instance.STATUS_UP),
                       Instance("xyz", "name", "address", Instance.STATUS_DOWN),
                       Instance("def", "name", "address", Instance.STATUS_UP)]

        dredd.patrol(instances_1)

        instances_2 = [Instance("abc", "name", "address", Instance.STATUS_UP),
                       Instance("xyz", "name", "address", Instance.STATUS_UP),
                       Instance("def", "name", "address", Instance.STATUS_UP)]

        dredd.patrol(instances_2)

        self.assertFalse(dredd.getsuspects())

    def test_count_suspects_failures(self):
        dredd = Dredd()

        instances = [Instance("abc", "name", "address", Instance.STATUS_UP),
                     Instance("xyz", "name", "address", Instance.STATUS_DOWN),
                     Instance("opq", "name", "address", Instance.STATUS_DOWN),
                     Instance("def", "name", "address", Instance.STATUS_UP)]

        dredd.patrol(instances)
        assert dredd.getsuspects()[0].failures == 1

        dredd.patrol(instances)
        assert dredd.getsuspects()[0].failures == 2

    def test_punish_suspects_with_too_many_failures(self):
        mock_cloud = Mock()
        mock_cloud.terminate = Mock()
        dredd = Dredd(cloud=mock_cloud)

        instances_1 = [Instance("abc", "name", "address", Instance.STATUS_UP),
                       Instance("xyz", "name", "address", Instance.STATUS_DOWN),
                       Instance("opq", "name", "address", Instance.STATUS_DOWN),
                       Instance("def", "name", "address", Instance.STATUS_UP)]

        instances_2 = [Instance("abc", "name", "address", Instance.STATUS_UP),
                       Instance("xyz", "name", "address", Instance.STATUS_DOWN),
                       Instance("opq", "name", "address", Instance.STATUS_UP),
                       Instance("def", "name", "address", Instance.STATUS_UP)]

        dredd.patrol(instances_1)
        dredd.patrol(instances_1)
        dredd.patrol(instances_2)

        mock_cloud.terminate.assert_called_with(instance_id=instances_1[1].id)
