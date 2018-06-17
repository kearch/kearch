from kearch_common._version import __version__


def wrap_json(payload, meta={}):
    return {
        'kearch_version': __version__,
        'meta': meta,
        'payload': payload,
    }


def get_payload(response):
    """Get `payload` as json object from `requests.Response` object."""
    j = response.json()
    if (j is None) or ('payload' not in j):
        return None
    return j['payload']
