import logging


class NoOp(object):
    def __init__(self, client=None):
        self.client = client

    def terminate(self, instance_id):
        logging.getLogger(__name__).info("Killing machine: %s" % instance_id)
