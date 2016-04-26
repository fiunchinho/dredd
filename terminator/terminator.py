import requests
import boto3
import logging
import time
import argparse


def build_eureka_url(region, url, ssl=False):
    if ssl:
        return 'https://' + region + '.' + url + '/v2/apps'
    else:
        return 'http://' + region + '.' + url + '/v2/apps'


def get_instances(url):
    r = requests.get(url, headers={'Accept': 'application/json'})
    applications = r.json()['applications']['application']

    instances = []

    for application in applications:
        for instance in application['instance']:
            metadata = instance.get('dataCenterInfo').get('metadata')
            if metadata:
                instance_id = metadata.get('instance-id')
            else:
                instance_id = None
            name = instance.get('vipAddress')
            dns = instance.get('hostName')
            asg = instance.get('asgName', None)
            status = instance.get('status')
            instances.append({'id': instance_id, 'name': name, 'dns': dns, 'asg': asg, 'status': status})

    return instances


def is_suspicious(instance_id, instances):
    return next((instance for instance in instances if instance['instance'] == instance_id), None)


def absolve_healthy_instances(instances, suspicious_instances):
    healthy_instances = [instance for instance in instances if instance['status'] == 'UP']
    return [instance for instance in suspicious_instances if instance not in healthy_instances]


def arrest_unhealthy_instances(instances, criminal_records):
    unhealthy_instances = [instance for instance in instances if instance['status'] == 'DOWN']
    for instance in unhealthy_instances:
        logger.info("Checking instance: %s" % instance)
        suspect_crimes = is_suspicious(instance['id'], criminal_records)
        if suspect_crimes:
            judge_suspect_crimes(suspect_crimes)
        else:
            criminal_records.append({'instance': instance['id'], 'crimes': 1})


def judge_suspect_crimes(suspect):
    suspect['crimes'] += 1
    if suspect['crimes'] >= 3:
        logger.info("Killing machine: %s" % suspect)
        # punish(suspect)


def punish(suspect):
    client.set_instance_health(
        InstanceId=suspect['id'],
        HealthStatus='Unhealthy',
        ShouldRespectGracePeriod=True
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--region', help='AWS Region', default='eu-west-1')
    parser.add_argument('-e','--eureka-url', help='Eureka endpoint', required=True)
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    client = boto3.client('autoscaling', region_name=args.region)
    criminal_record = []

    while True:
        instances = get_instances(build_eureka_url(args.region, args.eureka_url))
        absolve_healthy_instances(instances, criminal_record)
        arrest_unhealthy_instances(instances, criminal_record)

        duration = 3
        logger.info("Sleeping for %s seconds" % duration)
        time.sleep(duration)
