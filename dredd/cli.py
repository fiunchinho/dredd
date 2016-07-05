"""This module provides the main functionality of HTTPie.
Invocation flow:
  1. Read, validate and process the input (args, `stdin`).
  2. Create and send a request.
  3. Stream, and possibly process and format, the parts
     of the request-response exchange selected by output options.
  4. Simultaneously write to `stdout`
  5. Exit.
"""
import argparse
import logging
from logging.config import dictConfig
import time

# from dredd import Dredd
# from dredd.discovery.factory import Factory
# from dredd.cloud.factory import Factory as CloudFactory
# from discovery.factory import Factory
# from cloud.factory import Factory as CloudFactory
from discovery.factory import Factory
from cloud.factory import Factory as CloudFactory
from dredd import Dredd


def main():
    """
    The main function.
    Pre-process args, handle some special types of invocations,
    and run the main program with error handling.
    Return exit status code.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',
                        '--region',
                        help='AWS Region',
                        default='eu-west-1')
    parser.add_argument('-u',
                        '--discovery',
                        help='Type of discovery mechanism',
                        default='eureka')
    parser.add_argument('-e',
                        '--endpoint',
                        help='Endpoint returning list of instances',
                        required=True)
    parser.add_argument('-c',
                        '--cloud',
                        help='Cloud provider [aws, dry-run]',
                        default='dry-run')
    parser.add_argument('-i',
                        '--interval',
                        help='Interval',
                        default=3)
    parser.add_argument('-t',
                        '--crimes_threshold',
                        help='Number of consecutive crimes that must occur before punishing a suspect',
                        default=3)
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

    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        handlers={
            'default': {
                'level': args.loglevel,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        loggers={
            '': {
                'handlers': ['default'],
                'level': args.loglevel,
                'propagate': True
            }
        }
    )

    dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    discovery = Factory().get_discovery(args.discovery, args.endpoint)
    cloud = CloudFactory().get_cloud(name=args.cloud, region=args.region)
    dredd = Dredd(cloud=cloud)

    logger.info("Starting to patrol...")

    while True:
        dredd.patrol(instances=discovery.instances())
        logger.info("Sleeping for %s seconds" % args.interval)
        time.sleep(int(args.interval))


if __name__ == '__main__':
    main()
