# htc-api

Hack The Classroom game server API.

## Notes

- basic requests api client

## Staging

```python
from htc_api import Client

client = Client('vesche', 'acX2rUvbX')
client.solve('level_id', 'flag')
```