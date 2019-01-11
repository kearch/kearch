# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from sp_gateway_server.models.connection_request_on_sp import ConnectionRequestOnSP  # noqa: E501
from sp_gateway_server.models.document import Document  # noqa: E501
from sp_gateway_server.models.inline_response200 import InlineResponse200  # noqa: E501
from sp_gateway_server.models.summary import Summary  # noqa: E501
from sp_gateway_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_a_conenction_request_post(self):
        """Test case for add_a_conenction_request_post

        Add a connection request sent from meta server to specialist server.
        """
        connection_request_on_sp = ConnectionRequestOnSP()
        response = self.client.open(
            '/v0/sp/gateway/add_a_conenction_request',
            method='POST',
            data=json.dumps(connection_request_on_sp),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_a_conenction_request_delete(self):
        """Test case for delete_a_conenction_request_delete

        Delete a connection request sent from meta server to specialist server.
        """
        query_string = [('me_host', 'me_host_example')]
        response = self.client.open(
            '/v0/sp/gateway/delete_a_conenction_request',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_a_summary_get(self):
        """Test case for get_a_summary_get

        Get summary of this specialist server.
        """
        query_string = [('me_host', 'me_host_example')]
        response = self.client.open(
            '/v0/sp/gateway/get_a_summary',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_retrieve_get(self):
        """Test case for retrieve_get

        Retrieve search results.
        """
        query_string = [('queries', 'queries_example'),
                        ('max_urls', 56)]
        response = self.client.open(
            '/v0/sp/gateway/retrieve',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
