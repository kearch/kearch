import json
import urllib

from kearch_common.data_format import wrap_json


class KearchRequester(object):
    """Interface for communicating between containers or servers."""

    def __init__(self, host, port=None, requester_name='', conn_type='json'):
        super(KearchRequester, self).__init__()
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.requester_name = requester_name

    def request(self, path='', method='GET', payload={}, headers={}):
        url = urllib.parse.urljoin('{}:{}'.format(self.host, self.port), path)
        if method == 'GET':
            # GET の場合は payload を url param にする
            req = urllib.request.Request(
                '{}?{}'.format(url, urllib.parse.urlencode(payload)))
        else:
            # GET 以外は json に payload を含めて送る
            meta = {
                'requester': self.requester_name,
            }
            data = wrap_json(payload, meta)
            req = urllib.request.Request(
                url, json.dumps(data).encode(), headers)

        with urllib.request.urlopen(req) as res:
            response = json.load(res)

        return response
