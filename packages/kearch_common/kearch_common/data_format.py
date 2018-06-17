import urllib

from kearch_common._version import __version__


def wrap_json(payload, meta={}):
    return {
        'kearch_version': __version__,
        'meta': meta,
        'payload': payload,
    }


def wrap_get_param_str(payload):
    return


def get_payload(json):
    if (json is None) or ('payload' not in json):
        return None
    return json['payload']
