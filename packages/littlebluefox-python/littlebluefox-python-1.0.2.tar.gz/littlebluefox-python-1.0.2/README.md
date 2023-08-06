# LittleBlueFox pip package (python)

Push your security events on the LittleBlueFox.io API.

## Installation

```bash
$ pip3 install littlebluefox-python
```

## Usage

```python
from littlebluefox import LittleBlueFoxClient

access_token = '...'

lbf_client = LittleBlueFoxClient(access_token)

event = {
    'event_type': 'authentication_success',
    'uref': '42',
    'email': 'demo@demo.com',
    'remote_ip': '...',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    },
}

try:
  lbf_client.push(event)
except Exception as err:
  print('Error: {}'.format(err))
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/LittleBlueFox/littlebluefox-python.

```
$ python3 setup.py sdist bdist_wheel
$ python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
