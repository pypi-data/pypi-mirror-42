"""
Unittests
"""

import unittest


class TestCase(unittest.TestCase):
    """
    Parent class for all unittests.
    """
    pass


BASE_CONFIG = {
    "clusters": [
        {
            "name": "test-cluster",
            "cluster": {
                "server": "http://localhost:8080",
            }
        }
    ],
    "contexts": [
        {
            "name": "test-cluster",
            "context": {
                "cluster": "test-cluster",
                "user": "test-user",
            }
        }
    ],
    "users": [
        {
            'name': 'test-user',
            'user': {},
        }
    ],
    "current-context": "test-cluster",
}

