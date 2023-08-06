# -*- coding: utf-8 -*-
import collections

import grpc


class _ClientCallDetails(
    collections.namedtuple(
        '_ClientCallDetails', ('method', 'timeout', 'metadata', 'credentials')
    ), grpc.ClientCallDetails
):
    pass


class MetadataInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def intercept_unary_unary(
        self, continuation, client_call_details, request
    ):

        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)

        for k, v in self.metadata.items():
            metadata.append((k, v))

        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials
        )

        response = continuation(client_call_details, request)
        return response
