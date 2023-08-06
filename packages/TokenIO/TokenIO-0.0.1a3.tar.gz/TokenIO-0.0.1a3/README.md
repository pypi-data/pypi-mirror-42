# [Token](https://token.io) Python SDK

![PyPI](https://img.shields.io/pypi/v/TokenIO.svg?style=popout-square)

**The SDK is still under development, might be unstable, use at your own risk.**

The Python SDK for interacting with [TokenOS](https://developer.token.io/).

## Requirements

Python 3.5+

## Installation

```shell
$ pip install tokenio
```


## Example

```python
from tokenio import TokenClient
from tokenio.config import SandboxConfig
from tokenio.security.engines.memorycryptoengine import MemoryCryptoEngine
from tokenio.proto.alias_pb2 import Alias

dev_key = '4qY7lqQw8NOl9gng0ZHgT4xdiDqxqoGVutuZwrUYQsI'
config = SandboxConfig(dev_key=dev_key, crypto_engine=MemoryCryptoEngine)
client = TokenClient(config)

alias = Alias(type=Alias.EMAIL, value='your-email-address@example.com')
member = client.create_member(alias)
keys = member.get_keys()
print(keys)
```
