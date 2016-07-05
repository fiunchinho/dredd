from cloud.noop import NoOp
from instance import Instance
from suspect import Suspect

import logging


class Dredd(object):
    def __init__(self, cloud=NoOp(), max_crimes=3):
        self.instances = []
        self.suspects = []
        self.cloud = cloud
        self.max_crimes = max_crimes

    def patrol(self, instances):
        for instance in instances:
            logging.getLogger(__name__).debug("Instance %s is %s" % (instance.id, instance.status))
            if instance.status == Instance.STATUS_UP:
                self._absolve_recovered_suspects(instance)
            if instance.status == Instance.STATUS_DOWN:
                self._arrest(instance)

        self._judge_suspects_crimes()

    def punish(self, instance):
        self.cloud.terminate(instance_id=instance.id)

    def getsuspects(self):
        return self.suspects

    def _arrest(self, instance):
        reoffending_suspect = self._is_reoffending(instance)
        if reoffending_suspect:
            reoffending_suspect.failures += 1
            logging.getLogger(__name__).info("Increasing failures of instance %s (%s)" % (instance.id,
                                                                                          reoffending_suspect.failures))
        else:
            logging.getLogger(__name__).info("First failure of instance %s" % instance.id)
            self.suspects.append(Suspect(instance, 1))

    def _is_reoffending(self, instance):
        found_suspect = None
        for suspect in self.suspects:
            if suspect.instance.id == instance.id:
                found_suspect = suspect
                break
        return found_suspect

    def _absolve_recovered_suspects(self, instance):
        logging.getLogger(__name__).debug("Removing instance %s from suspects (if there is)" % instance.id)
        self.suspects = filter(lambda x: x.instance.id is not instance.id, self.suspects)

    def _judge_suspects_crimes(self):
        for suspect in self.suspects:
            if suspect.failures >= self.max_crimes:
                self.punish(suspect.instance)
