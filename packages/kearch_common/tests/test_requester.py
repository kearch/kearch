import unittest

from kearch_common.requester import KearchRequester


class TestRequester(unittest.TestCase):

    def test_get_request(self):
        requester = KearchRequester(
            'https://jsonplaceholder.typicode.com', requester_name='test_requester')
        requester.request(method='GET', path='/posts')
