import logging

import requests

from dredd.instance import Instance


class Eureka(object):
    def __init__(self, url):
        self.url = url

    def instances(self):
        r = requests.get(self.url, headers={'Accept': 'application/json'})
        applications = r.json()['applications']['application']

        instances = []

        for application in applications:
            for instance in application['instance']:
                metadata = instance.get('dataCenterInfo').get('metadata')
                if not metadata:
                    instance_id = instance.get('instanceId')
                    if not instance_id:
                        logging.getLogger(__name__).warn(
                            "Instance %s has no id or metadata. Skipping..." % instance.get('vipAddress'))
                        continue
                else:
                    instance_id = metadata.get('instance-id')

                instances.append(
                    Instance(
                        id=instance_id,
                        name=instance.get('vipAddress'),
                        dns=instance.get('hostName'),
                        asg=instance.get('asgName', None),
                        status=instance.get('status')
                    )
                )

        return instances
