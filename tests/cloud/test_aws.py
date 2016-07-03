from unittest import TestCase

from mock import Mock

from dredd.cloud.aws import Aws


class NoOpTest(TestCase):
    def test_aws_calls_http_client(self):
        instance_to_terminate = 'any-id'
        mock_client = self.given_boto_client()

        aws = Aws(mock_client)
        aws.terminate(instance_to_terminate)

        mock_client.set_instance_health.assert_called_with(InstanceId=instance_to_terminate,
                                                           HealthStatus='Unhealthy',
                                                           ShouldRespectGracePeriod=True)

    def given_boto_client(self):
        mock_client = Mock()
        mock_client.set_instance_health = Mock(return_value=True)

        return mock_client
