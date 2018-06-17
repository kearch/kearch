# kearch_common

## Installation

```sh
git clone https://github.com/akawashiro/kearch
cd kearch/packages/kearch_common
pip install -e .
```

## Usage

```python
requester = KearchRequester(
    'https://jsonplaceholder.typicode.com', requester_name='test_requester')
requester.request(method='GET', path='/posts')
```

## Testing

```sh
pytest
```
