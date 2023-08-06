"""
pykube.http unittests
"""
import copy
import logging

import mock
import pykube

from . import BASE_CONFIG, TestCase
from .fixtures import AUTHPLUGIN_FIXTURE


_log = logging.getLogger(__name__)


class TestHTTPClient(TestCase):
    def setUp(self):
        self.config = copy.deepcopy(BASE_CONFIG)

    def ensure_no_auth(self, client):
        self.assertIsNone(client.session.cert, msg="Should not send certs when not configured")
        self.assertNotIn("Authorization", client.session.headers, msg="Should not send basic auth when not configured")

    def test_no_auth_with_empty_user(self):
        """
        Cluster does not require any authentication--so no credentials are provided in the user info
        """
        config = {
            "clusters": [
                {
                    "name": "no-auth-cluster",
                    "cluster": {
                        "server": "http://localhost:8080",
                    }
                }
            ],
            "users": [
                {
                    "name": "no-auth-cluster",
                    "user": {}
                }
            ],
            "contexts": [
                {
                    "name": "no-auth-cluster",
                    "context": {
                        "cluster": "no-auth-cluster",
                        "user": "no-auth-cluster"
                    }
                }
            ],
            "current-context": "no-auth-cluster"
        }
        client = pykube.HTTPClient(pykube.KubeConfig(doc=config))
        self.ensure_no_auth(client)

    def test_no_auth_with_no_user(self):
        config = {
            "clusters": [
                {
                    "name": "no-auth-cluster",
                    "cluster": {
                        "server": "http://localhost:8080",
                    }
                }
            ],
            "contexts": [
                {
                    "name": "no-auth-cluster",
                    "context": {
                        "cluster": "no-auth-cluster"
                    }
                }
            ],
            "current-context": "no-auth-cluster"
        }
        client = pykube.HTTPClient(pykube.KubeConfig(doc=config))
        self.ensure_no_auth(client)


class TestHTTPAdapterSendMixin(TestCase):
    def setUp(self):
        self.config = copy.deepcopy(BASE_CONFIG)
        self.request = mock.Mock()
        self.request.headers = {}

    def test_build_session_bearer_token(self):
        """Test that HTTPClient correctly parses the token
        """
        self.config.update({
            'users': [
                {
                    'name': 'test-user',
                    'user': {
                        'token': 'test'
                    },
                },
            ]
        })
        _log.info('Built config: %s', self.config)

        adapter = pykube.http.KubernetesHTTPAdapterSendMixin()
        request, _ = adapter._setup_auth(self.request, pykube.KubeConfig(doc=self.config))
        _log.debug('Checking headers %s', request.headers)
        self.assertIn('Authorization', request.headers)
        self.assertEqual(request.headers['Authorization'], 'Bearer test')

    def test_exec_plugin_auth(self):
        self.config.update({
            'users': [
                {
                    'name': 'test-user',
                    'user': {
                        'exec': {
                            'command': 'heptio-authenticator-aws',
                            'apiVersion': 'client.authentication.k8s.io/v1alpha1',
                            'args': [
                                "token",
                                "-i",
                                "test-pykube-mock-eks-cluster"
                            ],
                        },
                    },
                },
            ]
        })
        _log.info('Built config: %s', self.config)
        with mock.patch('pykube.http.subprocess') as mock_subprocess:
            mock_subprocess.check_output = mock.Mock(return_value=AUTHPLUGIN_FIXTURE)
            adapter = pykube.http.KubernetesHTTPAdapterSendMixin()
            request, _ = adapter._setup_auth(self.request, pykube.KubeConfig(doc=self.config))
            _log.debug('Checking headers %s', request.headers)
            self.assertTrue(mock_subprocess.check_output.called)
            self.assertIn('Authorization', request.headers)
            self.assertEqual(request.headers['Authorization'], 'Bearer test')

