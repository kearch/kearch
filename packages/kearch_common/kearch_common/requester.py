import json
import urllib

import requests

from kearch_common.data_format import wrap_json


class KearchRequester(object):
    """Interface for communicating between containers or servers."""

    def __init__(self, host, port=None, requester_name='', conn_type='json'):
        super(KearchRequester, self).__init__()
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.requester_name = requester_name

    def request(self, path='', method='GET',
                params=None, payload=None,
                headers=None, timeout=None):
        if self.port is None:
            url = urllib.parse.urljoin(self.host, path)
        else:
            url = urllib.parse.urljoin(
                '{}:{}'.format(self.host, self.port), path)

        if method == 'GET':
            # GET の場合は payload を url param にする
            resp = requests.get(url, params=params, timeout=timeout)
        else:
            # GET 以外は json に payload を含めて送る
            meta = {
                'requester': self.requester_name,
            }
            data = wrap_json(payload, meta)
            resp = requests.request(
                method, url, params=params, json=data, timeout=timeout)

        return resp
