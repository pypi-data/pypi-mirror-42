# -*- coding: utf-8 -*-

__version__ = '0.0.1-alpha2'

__all__ = ["TokenClient"]

try:
    from tokenio.token_client import TokenClient
except ImportError:  # pragma: no cover
    pass  # pragma: no cover
