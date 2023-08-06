# -*- coding: utf-8 -*-
import collections

import time

import grpc

from tokenio import utils
from tokenio.proto.gateway.auth_pb2 import GrpcAuthPayload
from tokenio.rpc.authentication_context import AuthenticationContext
from tokenio.security.engines import CryptoEngine


class _ClientCallDetails(
    collections.namedtuple(
        '_ClientCallDetails', ('method', 'timeout', 'metadata', 'credentials')
    ), grpc.ClientCallDetails
):
    pass


class ClientAuthenticatorInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, member_id, crypto_engine: CryptoEngine):
        self.member_id = member_id
        self.crypto_engine = crypto_engine

    def intercept_unary_unary(
        self, continuation, client_call_details, request
    ):
        now = int(time.time() * 1000)
        payload = GrpcAuthPayload(
            request=request.SerializeToString(), created_at_ms=now
        )
        key_level = AuthenticationContext.reset_key_level()
        signer = self.crypto_engine.create_signer(key_level)
        signature = signer.sign_proto_message(payload)

        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(('token-realm', 'Token'))
        metadata.append(('token-scheme', 'Token-Ed25519-SHA512'))
        metadata.append(('token-key-id', signer.id))
        metadata.append(('token-signature', signature))
        metadata.append(('token-created-at-ms', str(now)))
        metadata.append(('token-member-id', self.member_id))

        on_behalf_of = AuthenticationContext.get_on_behalf_of()
        if on_behalf_of:
            metadata.append(('token-on-behalf-of', on_behalf_of))
            metadata.append(
                (
                    'customer-initiated',
                    AuthenticationContext.get_customer_initiated()
                )
            )
            AuthenticationContext.clear_access_token()

        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials
        )
        response = continuation(client_call_details, request)
        return response
