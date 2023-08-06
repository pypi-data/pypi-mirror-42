# -*- coding: utf-8 -*-
from tokenio import utils
from tokenio.config import Config
from tokenio.exceptions import InvalidStateException
from tokenio.member import Member
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.member_pb2 import PERSONAL, BUSINESS
from tokenio.proto.security_pb2 import Key
from tokenio.proto.token_pb2 import TokenRequestStatePayload
from tokenio.rpc.channel import Channel
from tokenio.rpc.client import Client
from tokenio.token_request import TokenRequestState, TokenRequestCallbackParameters, TokenRequestCallback


class TokenClient:
    TOKEN_REQUEST_TEMPLATE = '{url}/app/request-token/{request_id}?state={state}'

    def __init__(self, config: Config):
        self.channel = Channel.channel_factory(
            config.rpc_host, config.rpc_port, config.dev_key,
            config.rpc_use_ssl
        )
        self.CryptoEngine = config.crypto_engine
        self._unauthenticated_client = Client.unauthenticated(self.channel)
        self.config = config

    def is_alias_exists(self, alias: Alias) -> bool:
        return self._unauthenticated_client.alias_exists(alias)

    def get_member_id(self, alias: Alias) -> str:
        return self._unauthenticated_client.get_member_id(alias)

    def create_member(self, alias=None, member_type=PERSONAL):
        agent_id = self._unauthenticated_client.get_default_agent()
        member_id = self._unauthenticated_client.create_member_id(
            member_type=member_type
        )
        crypto_engine = self.CryptoEngine(member_id)
        operations = []
        metadata = []
        operations.append(
            utils.create_add_key_member_operation(
                crypto_engine.generate_key(Key.PRIVILEGED)
            )
        )
        operations.append(
            utils.create_add_key_member_operation(
                crypto_engine.generate_key(Key.STANDARD)
            )
        )
        operations.append(
            utils.create_add_key_member_operation(
                crypto_engine.generate_key(Key.LOW)
            )
        )
        operations.append(utils.create_recovery_agent_operation(agent_id))

        if alias is not None:
            operations.append(
                utils.create_add_alias_operation(utils.normalize_alias(alias))
            )
            metadata.append(
                utils.create_add_alias_operation_metadata(
                    utils.normalize_alias(alias)
                )
            )

        signer = crypto_engine.create_signer(Key.PRIVILEGED)
        created_member = self._unauthenticated_client.create_member(
            member_id=member_id,
            operations=operations,
            metadata=metadata,
            signer=signer
        )
        # assert created_member.id == member_id
        crypto_engine = self.CryptoEngine(created_member.id)
        client = Client.authenticated(
            self.channel, created_member.id, crypto_engine
        )
        member = Member(client)
        return member

    def create_business_member(self, alias):
        return self.create_member(alias, BUSINESS)

    def get_member(self, member_id):
        crypto_engine = self.CryptoEngine(member_id)
        client = Client.authenticated(self.channel, member_id, crypto_engine)
        # client.get_member(member_id)
        return Member(client)

    def get_banks(
        self,
        ids=None,
        search=None,
        country=None,
        page=None,
        per_page=None,
        sort=None,
        provider=None
    ):
        return self._unauthenticated_client.get_banks(
            ids, search, country, page, per_page, sort, provider
        )

    def generate_token_request_url(self, request_id, state='', csrf_token=''):
        csrf_token_hash = utils.hash_string(csrf_token)
        token_request_state = TokenRequestState(csrf_token_hash, state)
        return self.TOKEN_REQUEST_TEMPLATE.format(
            url=self.config.web_url,
            state=token_request_state.serialize(),
            request_id=request_id
        )

    def get_token_request_result(self, token_request_id):
        return self._unauthenticated_client.get_token_request_result(
            token_request_id
        )

    def retrieve_token_request(self, request_id):
        return self._unauthenticated_client.retrieve_token_request(request_id)

    def begin_recovery(self, alias):
        return self._unauthenticated_client.begin_recovery(alias)

    def get_recovery_authorization(
        self, verification_id, code, privileged_key
    ):
        return self._unauthenticated_client.get_recovery_authorization(
            verification_id, code, privileged_key
        )

    def complete_recovery(
        self, member_id, recovery_operations, privileged_key, crypto_engine
    ):
        updated_member = self._unauthenticated_client.complete_recovery(
            member_id, recovery_operations, privileged_key, crypto_engine
        )
        client = Client.authenticated(
            self.channel, updated_member.id, crypto_engine
        )
        return Member(client)

    def complete_recovery_with_default_rule(
        self, member_id, verification_id, code
    ):
        crypto_engine = self.CryptoEngine(member_id)
        recovered_member = self._unauthenticated_client.complete_recovery_with_default_rule(
            member_id, verification_id, code, crypto_engine
        )
        client = Client.authenticated(
            self.channel, recovered_member.id, crypto_engine
        )
        return Member(client)

    def parse_token_request_callback_url(self, callback_url, csrf_token=None):
        member = self._unauthenticated_client.get_token_member()
        parameters = TokenRequestCallbackParameters.create(callback_url)
        state = TokenRequestState.parse(parameters.state)
        if state.csrf_token_hash != utils.hash_string(csrf_token):
            raise InvalidStateException("InvalidStateException")

        payload = TokenRequestStatePayload(
            token_id=parameters.token_id, state=state.serialize()
        )
        utils.verify_signature(member, payload, parameters.signature)
        return TokenRequestCallback(parameters.token_id, state=state.state)
