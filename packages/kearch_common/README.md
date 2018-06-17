# kearch_common

## Installation

```sh
git clone https://github.com/akawashiro/kearch
cd kearch/packages/kearch_common
pip install -e .
```

## Usage

```python
from kearch_common.requester import KearchRequester

requester = KearchRequester(
    'https://jsonplaceholder.typicode.com', requester_name='test_requester')

# GET https://jsonplaceholder.typicode.com/posts?userId=1
resp = requester.request(method='GET', path='/posts', params={'userId': 1})

# POST https://jsonplaceholder.typicode.com/posts
payload = {'userId': 1, 'title': 'hello', 'body': 'world'}
resp = requester.request(method='POST', path='/posts', payload=payload)

# extract `payload` from response
from kearch_common.data_format import get_payload
payload_json = get_payload(resp)
```

See
https://github.com/requests/requests/blob/master/requests/models.py
for details of response.

## Testing

```sh
pytest
```
