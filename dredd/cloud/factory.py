import boto3

from aws import Aws
from noop import NoOp


class Factory(object):
    def get_cloud(self, name, region=None):
        if name == 'aws':
            return Aws(boto3.client('autoscaling', region_name=region))
        elif name == 'dry-run':
            return NoOp()
        else:
            raise NotImplementedError('Unknown discovery mechanism. Options are: eureka, consul')
