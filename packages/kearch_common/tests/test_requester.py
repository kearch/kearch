import unittest

from kearch_common.requester import KearchRequester


class TestRequester(unittest.TestCase):

    def test_get_request(self):
        requester = KearchRequester(
            'https://jsonplaceholder.typicode.com', requester_name='test_requester')
        resp = requester.request(
            method='GET', path='/posts', params={'userId': 1})
        print(resp.json())
        assert(resp.status_code == 200)

    def test_post_request(self):
        requester = KearchRequester(
            'https://jsonplaceholder.typicode.com', requester_name='test_requester')
        payload = {'userId': 1, 'title': 'hello', 'body': 'world'}
        resp = requester.request(
            method='POST', path='/posts', payload=payload)
        print(resp.json())
        assert(resp.status_code == 201)
