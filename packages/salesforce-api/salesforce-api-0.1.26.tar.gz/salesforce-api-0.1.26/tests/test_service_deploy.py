import pytest
from io import BytesIO
from salesforce_api import exceptions
from . import helpers


class TestServiceDeploy(helpers.BaseTest):
    def setup_instance(self, requests_mock, texts):
        self.register_uri(requests_mock, 'POST', '/services/Soap/m/{version}', response_list=[
            {'text': x, 'status_code': 200} if isinstance(x, str) else x
            for x in texts
        ])

    def _create_zip(self):
        return BytesIO()

    def test_create_successful(self, requests_mock):
        self.setup_instance(requests_mock, [
            helpers.get_data('deploy/create_success.txt')
        ])
        deployment = self.create_client().deploy.deploy(self._create_zip())
        assert  '123' == deployment.async_process_id

    def test_create_failure(self, requests_mock):
        self.setup_instance(requests_mock, [
            helpers.get_data('deploy/create_failure.txt')
        ])
        with pytest.raises(exceptions.DeployCreateError):
            self.create_client().deploy.deploy(self._create_zip())

    def test_full_successful(self, requests_mock):
        self.setup_instance(requests_mock, [
            helpers.get_data('deploy/create_success.txt'),
            helpers.get_data('deploy/status_pending.txt'),
            helpers.get_data('deploy/status_success.txt')
        ])
        deployment = self.create_client().deploy.deploy(self._create_zip())
        deployment.get_status()

    def test_cancel_successful(self, requests_mock):
        pass

    def test_full_failure(self, requests_mock):
        pass

    def test_code_coverage_failure(self, requests_mock):
        pass
