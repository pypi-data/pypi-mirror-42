from copy import deepcopy

import json
import mock

import pykube
from pykube.http import (
    AuthPluginFailed,
    AuthPluginExecFailed,
    AuthPluginParsingFailed,
    AuthPluginVersionFailed,
)

from . import BASE_CONFIG, TestCase
from .fixtures import AUTHPLUGIN_FIXTURE


class TestAuthExecPlugin(TestCase):
    def setUp(self):
        cfg = deepcopy(BASE_CONFIG)
        cfg.update({
            'users': [
                {
                    'name': 'test-user',
                    'user': {
                        'exec': {
                            'command': 'heptio-authenticator-aws',
                            'args': [
                                "token",
                                "-i",
                                "test-pykube-mock-eks-cluster"
                            ],
                            'apiVersion': 'client.authentication.k8s.io/v1alpha1',
                        },
                    },
                },
            ]
        })
        self.config = pykube.KubeConfig(doc=cfg)

    def test_builds_command(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        self.assertEquals(plugin.command, ["heptio-authenticator-aws", "token", "-i", "test-pykube-mock-eks-cluster"])

    def test_parse_raises_parsing_failed_on_invalid_json(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        invalid_json_output = "This is not json, just some string."
        with self.assertRaises(AuthPluginParsingFailed):
            plugin.parse(invalid_json_output)

    def test_parse_raises_parsing_failed_on_invalid_kind(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        invalid_kind_output = '{"kind": "something else entirely"}'
        with self.assertRaises(AuthPluginParsingFailed):
            plugin.parse(invalid_kind_output)

    def test_parse_raises_version_failed_if_not_expected_version(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        output = json.loads(AUTHPLUGIN_FIXTURE)
        output['apiVersion'] = 'this is not the expected api version'
        with self.assertRaises(AuthPluginVersionFailed):
            plugin.parse(json.dumps(output))

    def test_parse_raises_parsing_failed_if_no_api_version_in_output(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        output = json.loads(AUTHPLUGIN_FIXTURE)
        del output['apiVersion']
        with self.assertRaises(AuthPluginParsingFailed):
            plugin.parse(json.dumps(output))

    def test_execute_raises_exec_failed_if_subprocess_raises_exception(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        with mock.patch('pykube.http.subprocess') as mock_subprocess:
            mock_subprocess.check_output = mock.Mock(side_effect=Exception)
            with self.assertRaises(AuthPluginExecFailed):
                plugin.execute()

    def test_execute_raises_generic_failed_if_no_token_in_parsed_output(self):
        plugin = pykube.http.AuthExecPlugin(self.config)
        output = json.loads(AUTHPLUGIN_FIXTURE)
        del output['status']['token']
        with mock.patch('pykube.http.subprocess') as mock_subprocess:
            mock_subprocess.check_output = mock.Mock(return_value=json.dumps(output))
            with self.assertRaises(AuthPluginFailed):
                plugin.execute()
