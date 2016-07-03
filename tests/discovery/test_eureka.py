from unittest import TestCase
import responses

from dredd.discovery.eureka import Eureka


class EurekaTest(TestCase):
    @responses.activate
    def test_mark_unhealthy_as_suspicious(self):
        with open('tests/discovery/eureka_response.json', 'r') as response_file:
            response_body = response_file.read()

        responses.add(responses.GET,
                      'http://some_url',
                      body=response_body,
                      status=200,
                      content_type='application/json')

        eureka = Eureka('http://some_url')
        instances = eureka.instances()

        assert len(instances) == 8

        assert instances[0].id == "i-7eacfff4"
        assert instances[0].name == "eureka"
        assert instances[0].dns == "ec2-52-51-193-113.eu-west-1.compute.amazonaws.com"
        assert instances[0].asg is None
        assert instances[0].status == "UP"

        assert instances[7].id == "i-9a340110"
        assert instances[7].name == "ms-ij-api-monitor"
        assert instances[7].dns == "ec2-52-208-150-255.eu-west-1.compute.amazonaws.com"
        assert instances[7].asg == "ms_ij_api_monitor-v010"
        assert instances[7].status == "UP"

