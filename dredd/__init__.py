import argparse
import logging

import time

from discovery.factory import Factory
from cloud.factory import Factory as CloudFactory
from dredd import Dredd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',
                        '--region',
                        help='AWS Region',
                        default='eu-west-1')
    parser.add_argument('-d',
                        '--discovery',
                        help='Discovery mechanism',
                        default='eureka')
    parser.add_argument('-h',
                        '--url',
                        help='Discovery endpoint like http://eureka.io:8080/eureka-server/v2/apps',
                        required=True)
    parser.add_argument('-c',
                        '--cloud',
                        help='Cloud provider',
                        default='dry-run')
    parser.add_argument('-i',
                        '--interval',
                        help='Interval',
                        default=3)
    parser.add_argument('-t',
                        '--timeout',
                        help='Timeout',
                        default=5)
    parser.add_argument('-y',
                        '--unhealthy_threshold',
                        help='Unhealthy Threshold',
                        default=2)
    parser.add_argument('-z',
                        '--healthy_threshold',
                        help='Healthy Threshold',
                        default=5)
    parser.add_argument('-d',
                        '--debug',
                        help="Print lots of debugging statements",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.WARNING)
    parser.add_argument('-v',
                        '--verbose',
                        help="Be verbose",
                        action="store_const",
                        dest="loglevel",
                        const=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    logger = logging.getLogger(__name__)
    # logger.setLevel(args.loglevel)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    discovery = Factory().get_discovery(args.discovery, args.url)
    cloud = CloudFactory().get_cloud(name=args.cloud, region=args.region)
    dredd = Dredd(cloud=cloud)

    while True:
        dredd.patrol(instances=discovery.instances())
        logger.info("Sleeping for %s seconds" % args.interval)
        time.sleep(args.interval)
