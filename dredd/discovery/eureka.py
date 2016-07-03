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

                instances.append(
                    Instance(
                        id=metadata.get('instance-id'),
                        name=instance.get('vipAddress'),
                        dns=instance.get('hostName'),
                        asg=instance.get('asgName', None),
                        status=instance.get('status')
                    )
                )

        return instances
