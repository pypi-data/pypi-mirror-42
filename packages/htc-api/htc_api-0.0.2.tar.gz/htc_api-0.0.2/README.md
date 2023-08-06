# htc-api

Hack The Classroom game server API used by the client for web requests.

## How do?

```
pip install htc_api
```

```python
from htc_api import Client

client = Client('Bob', '069420')

if client.validate()['success']:
    client.solve('test', 'testflag')
    print(client.score())
```