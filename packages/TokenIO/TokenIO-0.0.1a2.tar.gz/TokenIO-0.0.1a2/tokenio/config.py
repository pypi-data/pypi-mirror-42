# -*- coding: utf-8 -*-
from tokenio.security.engines.memorycryptoengine import MemoryCryptoEngine


class Config:
    def __init__(
        self,
        rpc_host,
        rpc_port,
        web_url,
        dev_key,
        crypto_engine,
        rpc_use_ssl=True
    ):
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.web_url = web_url
        self.rpc_use_ssl = rpc_use_ssl
        self.dev_key = dev_key
        self.crypto_engine = crypto_engine


class ProductionConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.token.io',
            rpc_port=443,
            web_url='https://web-app.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class IntegrationConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.int.token.io',
            rpc_port=443,
            web_url='https://web-app.int.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class SandboxConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.sandbox.token.io',
            rpc_port=443,
            web_url='https://web-app.sandbox.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class StagingConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.stg.token.io',
            rpc_port=443,
            web_url='https://web-app.stg.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class PerformanceConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.perf.token.io',
            rpc_port=443,
            web_url='https://web-app.perf.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class DevelopmentConfig(Config):
    def __init__(self, dev_key, crypto_engine):
        super().__init__(
            rpc_host='api-grpc.dev.token.io',
            rpc_port=443,
            web_url='https://web-app.dev.token.io',
            crypto_engine=crypto_engine,
            rpc_use_ssl=True,
            dev_key=dev_key
        )


class TestConfig(SandboxConfig):
    def __init__(self):
        super().__init__(
            '4qY7lqQw8NOl9gng0ZHgT4xdiDqxqoGVutuZwrUYQsI', MemoryCryptoEngine
        )
