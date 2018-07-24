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
        if self.conn_type == 'json':
            return self.request_json(path, method, params, payload,
                                     headers, timeout)
        elif self.conn_type == 'sql':
            return self.request_sql(path, method, params, payload,
                                    headers, timeout)
        else:
            raise ValueError('conn_type should be "json" or "sql".')

    def request_json(self, path='', method='GET',
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

    def request_sql(self, path='', method='GET',
                    params=None, payload=None,
                    headers=None, timeout=None):
        parsed = urllib.parse.urlparse(path)
        parsed_path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if parsed_path == '/push_webpage_to_database':
            pass
        elif parsed_path == '/get_next_urls':
            pass
        elif parsed_path == '/push_links_to_queue':
            pass
        elif parsed_path == '/crawl_a_page':
            pass
        else:
            raise ValueError('Invalid path: {}'.format(path))
