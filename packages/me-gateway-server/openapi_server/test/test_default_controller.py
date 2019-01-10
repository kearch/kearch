# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.models.connection_request_on_me import ConnectionRequestOnME  # noqa: E501
from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from openapi_server.models.summary import Summary  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_a_conenction_request_post(self):
        """Test case for add_a_conenction_request_post

        Add a connection request sent from specialist server to meta server.
        """
        connection_request_on_me = ConnectionRequestOnME()
        response = self.client.open(
            '/v0/me/gateway/add_a_conenction_request',
            method='POST',
            data=json.dumps(connection_request_on_me),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_a_summary_post(self):
        """Test case for add_a_summary_post

        Add a summary to meta server.
        """
        summary = Summary()
        response = self.client.open(
            '/v0/me/gateway/add_a_summary',
            method='POST',
            data=json.dumps(summary),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_a_conenction_request_delete(self):
        """Test case for delete_a_conenction_request_delete

        Delete a connection request sent from specialist server to this meta server.
        """
        query_string = [('sp_host', 'sp_host_example')]
        response = self.client.open(
            '/v0/me/gateway/delete_a_conenction_request',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_retrieve_get(self):
        """Test case for retrieve_get

        Retrieve search results.
        """
        query_string = [('queries', 'queries_example'),
                        ('max_urls', 56),
                        ('sp_host', 'sp_host_example')]
        response = self.client.open(
            '/v0/me/gateway/retrieve',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
