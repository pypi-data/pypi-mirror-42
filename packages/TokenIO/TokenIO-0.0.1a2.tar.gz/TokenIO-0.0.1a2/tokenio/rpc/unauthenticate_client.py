# -*- coding: utf-8 -*-
from typing import Union

from tokenio import utils
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.gateway.gateway_pb2 import *
from tokenio.proto.member_pb2 import Member, MemberOperation, MemberUpdate
from tokenio.proto.security_pb2 import Key, Signature
from tokenio.proto.token_pb2 import TokenMember
from tokenio.security.engines import CryptoEngine


class UnauthenticatedClient:
    def __init__(self, channel):
        self._unauthenticated_channel = channel

    def alias_exists(self, alias: Alias) -> bool:
        return self._resolve_alias(alias).id != ''

    def _resolve_alias(self, alias: Alias) -> TokenMember:
        request = ResolveAliasRequest(alias=alias)

        with self._unauthenticated_channel as channel:
            response = channel.stub.ResolveAlias(request)
        return response.member

    def get_member_id(self, alias: Alias) -> Union[str, None]:
        member = self._resolve_alias(alias)
        if member.id == '':
            return None
        return member.id

    def get_member(self, member_id: str) -> Member:
        request = GetMemberRequest(member_id=member_id)

        with self._unauthenticated_channel as channel:
            response = channel.stub.GetMember(request)
        return response.member

    # PERSONAL, BUSINESS, TRANSIENT
    def create_member_id(
        self, member_type, token_request_id: Union[str, None] = None
    ):
        nonce = utils.generate_nonce()
        request = CreateMemberRequest(nonce=nonce, member_type=member_type)
        if token_request_id is not None:
            request.token_request_id = token_request_id

        with self._unauthenticated_channel as channel:
            response = channel.stub.CreateMember(request)
        return response.member_id

    def create_member(self, member_id, operations, metadata, signer):
        update = MemberUpdate(member_id=member_id, operations=operations)
        signature = Signature(
            key_id=signer.id,
            member_id=member_id,
            signature=signer.sign_proto_message(update)
        )
        request = UpdateMemberRequest(
            update=update, update_signature=signature, metadata=metadata
        )
        # print("REQUEST: " + utils.proto_message_to_bytes(request).decode())
        with self._unauthenticated_channel as channel:
            response = channel.stub.UpdateMember(request)
        return response.member

    def get_token_member(self):
        alias = Alias(type=Alias.DOMAIN, value='token.io', realm='token')
        member_id = self.get_member_id(alias)
        if member_id == '':
            return None

        return self.get_member(member_id)

    def get_banks(
        self,
        ids=None,
        search=None,
        country=None,
        page=None,
        per_page=None,
        sort=None,
        provider=None
    ) -> GetBanksResponse:
        request = GetBanksRequest()
        if ids is not None:
            request.ids = ids
        if search is not None:
            request.search = search
        if country is not None:
            request.country = country
        if page is not None:
            request.page = page
        if per_page is not None:
            request.per_page = per_page
        if sort is not None:
            request.sort = sort
        if provider is not None:
            request.provider = provider

        with self._unauthenticated_channel as channel:
            response = channel.stub.GetBanks(request)
        return response

    def retrieve_token_request(self, token_request_id):
        request = RetrieveTokenRequestRequest(request_id=token_request_id)

        with self._unauthenticated_channel as channel:
            response = channel.stub.RetrieveTokenRequest(request)
        return response.token_request

    def get_token_request_result(self, token_request_id):
        request = GetTokenRequestResultRequest(
            token_request_id=token_request_id
        )

        with self._unauthenticated_channel as channel:
            response = channel.stub.GetTokenRequestResult(request)
        return response

    def get_default_agent(self) -> str:
        alias = Alias(type=Alias.DOMAIN, value='token.io')
        request = ResolveAliasRequest(alias=alias)

        with self._unauthenticated_channel as channel:
            response = channel.stub.ResolveAlias(request)
        return response.member.id

    def begin_recovery(self, alias):
        alias = utils.normalize_alias(alias)
        request = BeginRecoveryRequest(alias=alias)
        with self._unauthenticated_channel as channel:
            response = channel.stub.BeginRecovery(request)
        return response.verification_id

    def complete_recovery_with_default_rule(
        self, member_id, verification_id, code, crypto_engine: CryptoEngine
    ):
        privileged_key = crypto_engine.generate_key(Key.PRIVILEGED)
        standard_key = crypto_engine.generate_key(Key.STANDARD)
        low_key = crypto_engine.generate_key(Key.LOW)

        signer = crypto_engine.create_signer(Key.PRIVILEGED)

        complete_request = CompleteRecoveryRequest(
            verification_id=verification_id, code=code, key=privileged_key
        )
        with self._unauthenticated_channel as channel:
            complete_response = channel.stub.CompleteRecovery(complete_request)

        member_request = GetMemberRequest(member_id=member_id)
        with self._unauthenticated_channel as channel:
            member_response = channel.stub.GetMember(member_request)

        member_recovery_operation = MemberOperation(
            recover=complete_response.recovery_entry
        )
        operations = utils.to_add_key_operations(
            [privileged_key, standard_key, low_key]
        )
        operations.append(member_recovery_operation)

        member_update = MemberUpdate(
            member_id=member_id,
            prev_hash=member_response.member.last_hash,
            operations=operations
        )

        signature = Signature(
            key_id=signer.id,
            member_id=member_id,
            signature=signer.sign_proto_message(member_update)
        )

        update_member_request = UpdateMemberRequest(
            update=member_update, update_signature=signature
        )
        with self._unauthenticated_channel as channel:
            member_update_response = channel.stub.UpdateMember(
                update_member_request
            )

        return member_update_response.member

    def get_recovery_authorization(
        self, verification_id, code, privileged_key
    ):
        request = CompleteRecoveryRequest(
            verification_id=verification_id, code=code, key=privileged_key
        )
        with self._unauthenticated_channel as channel:
            response = channel.stub.CompleteRecovery(request)
        # TODO: VerificationException
        return response.recovery_entry

    def complete_recovery(
        self, member_id, recovery_operations, privileged_key,
        crypto_engine: CryptoEngine
    ):
        standard_key = crypto_engine.generate_key(Key.STANDARD)
        low_key = crypto_engine.generate_key(Key.LOW)

        signer = crypto_engine.create_signer(Key.PRIVILEGED)
        operations = []
        for recovery_operation in recovery_operations:
            member_operation = MemberOperation(recover=recovery_operation)
            operations.append(member_operation)
        operations.extend(
            utils.to_add_key_operations(
                [privileged_key, standard_key, low_key]
            )
        )

        get_member_request = GetMemberRequest(member_id=member_id)
        with self._unauthenticated_channel as channel:
            get_member_response = channel.stub.GetMember(get_member_request)
        member_update = MemberUpdate(
            member_id=member_id,
            prev_hash=get_member_response.member.last_hash,
            operations=operations
        )

        signature = Signature(
            key_id=signer.id,
            member_id=member_id,
            signature=signer.sign_proto_message(member_update)
        )

        update_member_request = UpdateMemberRequest(
            update=member_update, update_signature=signature
        )
        with self._unauthenticated_channel as channel:
            member_update_response = channel.stub.UpdateMember(
                update_member_request
            )

        return member_update_response.member
