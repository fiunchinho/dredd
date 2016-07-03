# import requests
# import boto3
# import logging
# import time
# import argparse
#
#
# def build_eureka_url(region, url, ssl=False):
#     if ssl:
#         return 'https://' + region + '.' + url + '/v2/apps'
#     else:
#         return 'http://' + region + '.' + url + '/v2/apps'
#
#
# def get_instances(url):
#     r = requests.get(url, headers={'Accept': 'application/json'})
#     applications = r.json()['applications']['application']
#
#     instances = []
#
#     for application in applications:
#         for instance in application['instance']:
#             metadata = instance.get('dataCenterInfo').get('metadata')
#             if metadata:
#                 instance_id = metadata.get('instance-id')
#             else:
#                 instance_id = None
#             name = instance.get('vipAddress')
#             dns = instance.get('hostName')
#             asg = instance.get('asgName', None)
#             status = instance.get('status')
#             instances.append({'id': instance_id, 'name': name, 'dns': dns, 'asg': asg, 'status': status})
#
#     return instances
#
#
# def is_suspicious(instance_id, instances):
#     return next((instance for instance in instances if instance['instance'] == instance_id), None)
#
#
# def absolve_healthy_instances(instances, suspicious_instances):
#     healthy_instances = [instance for instance in instances if instance['status'] == 'UP']
#     return [instance for instance in suspicious_instances if instance not in healthy_instances]
#
#
# def arrest_unhealthy_instances(instances, criminal_records):
#     unhealthy_instances = [instance for instance in instances if instance['status'] == 'DOWN']
#     for instance in unhealthy_instances:
#         logger.info("Checking instance: %s" % instance)
#         suspect_crimes = is_suspicious(instance['id'], criminal_records)
#         if suspect_crimes:
#             judge_suspect_crimes(suspect_crimes)
#         else:
#             criminal_records.append({'instance': instance['id'], 'crimes': 1})
#             ec2 = boto3.client('ec2', region_name=args.region)
#             # ec2.Tag(instance['id'], 'failed_healthchecks', 1)
#             # ec2.create_tags(
#             #     Resources=instance['id'],
#             #     Tags=[{'Key': 'failed_healthchecks', 'Value': 1}]
#             # )

from suspect import Suspect

import logging


class Dredd(object):
    def __init__(self, cloud=None, max_crimes=3):
        self.instances = []
        self.suspects = []
        self.cloud = cloud
        self.max_crimes = max_crimes

    def patrol(self, instances):
        # healthy_instances = filter(lambda instance: instance.status is 'healthy', instances)
        # unhealthy_instances = filter(lambda instance: instance.status is 'unhealthy', instances)
        #
        # map(lambda instance: self.absolve_healthy_suspects(instance), healthy_instances)

        for instance in instances:
            if instance.status == 'healthy':
                logging.getLogger(__name__).info("Removing instance %s with status %s from suspects" % (instance.id,
                                                 instance.status))
                self.suspects = filter(lambda x: x.instance.id is not instance.id, self.suspects)
            if instance.status == 'unhealthy':
                found_suspect = None
                for suspect in self.suspects:
                    if suspect.instance.id == instance.id:
                        found_suspect = suspect
                        break

                if found_suspect:
                    found_suspect.failures += 1
                    logging.getLogger(__name__).info("Increasing failures of instance %s (%s)" % (instance.id,
                                                     found_suspect.failures))
                else:
                    logging.getLogger(__name__).info("First failure of instance %s" % instance.id)
                    self.suspects.append(Suspect(instance, 1))

        self._judge_suspects_crimes()

    def punish(self, instance):
        self.cloud.terminate(instance_id=instance.id)

    def getsuspects(self):
        return self.suspects

    def _judge_suspects_crimes(self):
        for suspect in self.suspects:
            if suspect.failures >= self.max_crimes:
                self.punish(suspect.instance)
