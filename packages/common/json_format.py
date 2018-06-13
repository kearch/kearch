from kearch_common.version import __version__


def wrap_json(payload, meta={}):
    return {
        'kearch_version': __version__,
        'meta': meta,
        'payload': payload,
    }


def get_payload(json):
    if (json is None) or ('payload' not in json):
        return None
    return json['payload']
