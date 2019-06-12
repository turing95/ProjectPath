# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPathController(BaseTestCase):
    """PathController integration test stubs"""

    def test_get_related_paths(self):
        """Test case for get_related_paths

        Returns related paths
        """
        query_string = [('limit', 789),
                        ('offset', 789)]
        response = self.client.open(
            '/api/v1/path/{pathId}/related'.format(pathId=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
