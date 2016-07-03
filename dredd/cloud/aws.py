import logging


class Aws(object):
    def __init__(self, client):
        self.client = client

    def terminate(self, instance_id):
        logging.getLogger(__name__).info("Killing machine: %s" % instance_id)
        self.client.set_instance_health(
            InstanceId=instance_id,
            HealthStatus='Unhealthy',
            ShouldRespectGracePeriod=True
        )
