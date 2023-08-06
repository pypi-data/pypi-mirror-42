# -*- coding: utf-8 -*-
import json
from urllib.parse import quote, urlsplit, parse_qs

from tokenio import utils
from tokenio.exceptions import CallbackParametersError
from tokenio.proto.security_pb2 import Signature


class TokenRequest:
    def __init__(self, token_payload, options, user_ref_id, customization_id):
        self.token_payload = token_payload
        self.options = options
        self.user_ref_id = user_ref_id  # TODO: default value?
        self.customization_id = customization_id  # ?

    @staticmethod
    def builder(token_payload):
        return TokenRequestBuilder(token_payload)


class TokenRequestBuilder:
    def __init__(self, token_payload):
        self.token_payload = token_payload
        self.options = {}
        self.user_ref_id = None
        self.customization_id = None

    def add_option(self, option, value):
        self.options[option] = value
        return self

    def add_all_options(self, **options):
        self.options.update(options)
        return self

    def set_user_ref_id(self, user_ref_id):
        self.user_ref_id = user_ref_id
        return self

    def set_customization_id(self, customization_id):
        self.customization_id = customization_id
        return self

    def build(self):
        return TokenRequest(
            self.token_payload, self.options, self.user_ref_id,
            self.customization_id
        )


class TokenRequestResult:
    def __init__(self, token_id, signature):
        self.token_id = token_id
        self.signature = signature


class TokenRequestCallback:
    def __init__(self, token_id, state):
        self.token_id = token_id
        self.state = state


class TokenRequestState:
    def __init__(self, csrf_token_hash, state):
        self.csrf_token_hash = csrf_token_hash
        self.state = state

    def serialize(self):
        data = {'csrf_token_hash': self.csrf_token_hash, 'state': self.state}
        return quote(utils.dict_to_bytes(data).decode())

    @classmethod
    def parse(cls, state_json):
        return cls(state_json['csrf_token_hash'], state_json['state'])


class TokenRequestCallbackParameters:
    TOKEN_ID_FIELD = 'tokenId'
    STATE_FIELD = 'state'
    SIGNATURE_FIELD = 'signature'

    def __init__(self, token_id, state, signature):
        self.token_id = token_id
        self.signature = signature
        self.state = state

    @classmethod
    def create(cls, callback_url):
        query = urlsplit(callback_url).query
        params = {k: v[0] for k, v in parse_qs(query).items()}
        if cls.TOKEN_ID_FIELD not in params or cls.STATE_FIELD not in params:
            raise CallbackParametersError(
                "Invalid or missing parameters in token request query."
            )
        token_id = params[cls.TOKEN_ID_FIELD]
        state_json = json.loads(params[cls.STATE_FIELD])

        signature_json = json.loads(params[cls.SIGNATURE_FIELD])
        signature = Signature(
            member_id=signature_json['memberId'],
            key_id=signature_json['keyId'],
            signature=signature_json['signature']
        )
        return cls(token_id, state_json, signature)
