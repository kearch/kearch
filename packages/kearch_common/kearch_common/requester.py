from kearch_common.json_format import wrap_json


class KearchRequester(object):
    """Interface for communicating between containers or servers."""

    def __init__(self, host, port, requester_name, conn_type='json'):
        super(KearchRequester, self).__init__()
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.requester_name = requester_name

    def request(self, payload, path='', method='GET'):
        meta = {
            'requester': self.requester_name,
        }
        data = wrap_json(payload, meta)
        # TODO(gky360): send data
        # TODO(gky360): return response
