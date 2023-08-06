# -*- coding: utf-8 -*-
import grpc

import tokenio
from tokenio.exceptions import RequestError
from tokenio.proto.gateway.gateway_pb2_grpc import GatewayServiceStub
from tokenio.rpc.interceptor.metadata_interceptor import MetadataInterceptor


class Channel:
    def __init__(self, host, port, use_ssl, *interceptors):
        self.rpc_uri = "{}:{}".format(host, port)
        self._channel = None
        self.use_ssl = use_ssl
        self.interceptors = interceptors

    @property
    def stub(self):
        if self.use_ssl:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel(self.rpc_uri, credentials)
        else:
            self._channel = grpc.insecure_channel(self.rpc_uri)
        intercept_channel = grpc.intercept_channel(
            self._channel, *self.interceptors
        )
        stub = GatewayServiceStub(intercept_channel)
        return stub

    @classmethod
    def channel_factory(cls, host, port, dev_key, use_ssl=True):
        def create_channel_with_interceptors(*interceptors):
            metadata_interceptor = MetadataInterceptor(
                {
                    'token-sdk': 'python',
                    'token-sdk-version': tokenio.__version__,
                    'token-dev-key': dev_key
                }
            )
            return cls(
                host, port, use_ssl, metadata_interceptor, *interceptors
            )

        return create_channel_with_interceptors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.close()
        if exc_type is not None and issubclass(exc_type, grpc.RpcError):
            raise RequestError(
                exc_val.code(), exc_val.details(), exc_val.debug_error_string()
            )
        return False
