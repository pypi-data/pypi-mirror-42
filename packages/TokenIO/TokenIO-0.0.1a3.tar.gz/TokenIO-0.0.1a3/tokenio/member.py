# -*- coding: utf-8 -*-
import copy
from typing import List, Optional, Union

from tokenio import utils
from tokenio.account import Account
from tokenio.exceptions import InvalidRealmException
from tokenio.proto.address_pb2 import Address
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.blob_pb2 import Blob, Attachment
from tokenio.proto.gateway.gateway_pb2 import GetTokensRequest
from tokenio.proto.member_pb2 import MemberAliasOperation, MemberOperation, MemberRemoveKeyOperation, RecoveryRule, \
    MemberRecoveryRulesOperation, AddressRecord, TrustedBeneficiary, MemberRecoveryOperation
from tokenio.proto.money_pb2 import Money
from tokenio.proto.security_pb2 import Key
from tokenio.proto.token_pb2 import TokenRequest, Token, TokenPayload
from tokenio.proto.transfer_pb2 import TransferPayload
from tokenio.proto.transferinstructions_pb2 import TransferEndpoint
from tokenio.rpc.authenticated_client import AuthenticatedClient
from tokenio.transfer_token_builder import TransferTokenBuilder


class Member:
    def __init__(self, client: AuthenticatedClient):
        self.client = client
        self.member_id = client.member_id

    def get_last_hash(self):
        return self.client.get_member(self.member_id).last_hash

    def get_aliases(self):
        return self.client.get_aliases()

    def get_first_alias(self):
        aliases = self.get_aliases()
        if len(aliases) == 0:
            return None
        return aliases[0]

    def get_keys(self):
        return self.client.get_member(self.member_id).keys

    def get_accounts(self):
        accounts = self.client.get_accounts()
        result = [Account(self, account, self.client) for account in accounts]
        return result

    def get_account(self, account_id):
        account = self.client.get_account(account_id)
        return Account(self, account, self.client)

    def get_balance(self, account_id: str, key_level: int):
        return self.client.get_balance(account_id, key_level)

    def get_current_balance(self, account_id: str, key_level: int):
        return self.client.get_balance(account_id, key_level).current

    def get_bank_info(self, bank_id):
        return self.client.get_bank_info(bank_id)

    def get_available_balance(self, account_id: str, key_level: int):
        return self.client.get_balance(account_id, key_level).available

    def get_balances(self, account_id: str, key_level: int):
        return self.client.get_balances(account_id, key_level)

    def get_transaction(self, account_id, transaction_id, key_level):
        return self.client.get_transaction(
            account_id, transaction_id, key_level
        )

    def get_transactions(self, account_id, key_level, limit, offset=None):
        return self.client.get_transactions(
            account_id, key_level, limit, offset
        )

    def get_token(self, token_id):
        return self.client.get_token(token_id)

    def remove_aliases(self, alias_list: List[Alias]):
        operations = []
        for alias in alias_list:
            alias_operations = MemberAliasOperation(
                alias_hash=utils.hash_alias(alias)
            )
            operation = MemberOperation(remove_alias=alias_operations)
            operations.append(operation)
        member = self.client.get_member(self.member_id)
        updated_member = self.client.update_member(member, operations, [])
        return updated_member.ByteSize() != 0

    def remove_alias(self, alias):
        return self.remove_aliases([alias])

    def add_aliases(self, alias_list: List[Alias]):
        operations = []
        metadata = []
        member = self.client.get_member(self.member_id)
        for alias in alias_list:
            partner_id = member.partner_id
            if partner_id and partner_id != 'token':
                if alias.realm and alias.realm != partner_id:
                    raise InvalidRealmException(
                        "Invalid realm {}; expected: {}".format(
                            alias.realm, partner_id
                        )
                    )
                alias.realm = partner_id
            operations.append(
                utils.create_add_alias_operation(utils.normalize_alias(alias))
            )
            metadata.append(
                utils.create_add_alias_operation_metadata(
                    utils.normalize_alias(alias)
                )
            )
        updated_member = self.client.update_member(
            member, operations, metadata
        )
        return updated_member.ByteSize() != 0

    def add_alias(self, alias):
        return self.add_aliases([alias])

    def for_access_token(self, token_id, customer_initiated=True):
        # TODO: test
        cloned = copy.deepcopy(self.client)
        cloned.use_access_token(token_id, customer_initiated)
        return Member(cloned)

    def store_token_request(self, token_request: TokenRequest):
        return self.client.store_token_request(
            token_request.token_payload, token_request.options,
            token_request.user_ref_id, token_request.customization_id
        )

    def get_transfer(self, transfer_id: str):
        return self.client.get_transfer(transfer_id)

    def get_transfers(
        self,
        limit: int,
        offset: Optional[str] = None,
        token_id: Optional[str] = None
    ):
        return self.client.get_transfers(limit, offset, token_id)

    def cancel_token(self, token: Token):
        return self.client.cancel_token(token)

    def sign_token_request_state(
        self, token_request_id: str, token_id: str, state: str
    ):
        return self.client.sign_token_request_state(
            token_request_id, token_id, state
        )

    def create_blob(
        self,
        owner_id: str,
        type: str,
        name: str,
        data: bytes,
        access_mode: int = Blob.DEFAULT
    ) -> Attachment:
        payload = Blob.Payload(
            owner_id=owner_id,
            name=name,
            type=type,
            data=data,
            access_mode=access_mode
        )
        blob_id = self.client.create_blob(payload)
        attachment = Attachment(blob_id=blob_id, name=name, type=type)
        return attachment

    def redeem_token(
        self,
        token: Token,
        amount: Union[int, float],
        currency: Optional[str],
        description: Optional[str],
        destination: Optional[TransferEndpoint] = None,
        ref_id: Optional[str] = None
    ):
        payload = TransferPayload(
            token_id=token.id, description=token.payload.description
        )
        if destination is not None:
            payload.destinations.extend([destination])

        if amount is not None:
            money = Money(value=str(amount))
            payload.amount.CopyFrom(money)

        if currency is not None:
            if payload.amount.ByteSize():
                payload.amount.currency = currency
            else:
                money = Money(currency=currency)
                payload.amount.CopyFrom(money)

        if description is not None:
            payload.description = description

        if ref_id is not None:
            payload.ref_id = ref_id
        else:
            payload.ref_id = utils.generate_nonce()

        return self.client.create_transfer(payload)

    def __update_keys(self, operations):
        latest_member = self.client.get_member(self.member_id)
        updated_member = self.client.update_member(latest_member, operations)
        return updated_member.ByteSize() != 0

    def approve_keys(self, keys: List[Key]) -> bool:
        operations = []
        for key in keys:
            operations.append(utils.create_add_key_member_operation(key))
        return self.__update_keys(operations)

    def approve_key(self, key: Key):
        return self.approve_keys([key])

    def remove_keys(self, key_ids: List[str]) -> bool:
        operations = []
        for key_id in key_ids:
            operations.append(MemberRemoveKeyOperation(key_id=key_id))
        return self.__update_keys(operations)

    def remove_key(self, key_id):
        return self.remove_keys([key_id])

    def delete_member(self):
        return self.client.delete_member()

    def set_profile(self, profile):
        return self.client.set_profile(profile)

    def set_profile_picture(self, type: str, data: bytes):
        payload = Blob.Payload(
            owner_id=self.member_id,
            type=type,
            name='profile',
            data=data,
            access_mode=Blob.PUBLIC
        )
        return self.client.set_profile_picture(payload)

    def get_profile(self, member_id):
        return self.client.get_profile(member_id)

    def get_profile_picture(self, member_id: str, size: int):
        return self.client.get_profile_picture(member_id, size)

    def verify_alias(self, verification_id: str, code: str):
        return self.client.verify_alias(verification_id, code)

    def retry_verification(self, alias: Alias):
        return self.client.retry_verification(alias)

    def add_recovery_rule(self, recovery_rule: RecoveryRule):
        member = self.client.get_member(self.member_id)
        recovery_operation = MemberRecoveryRulesOperation(
            recovery_rule=recovery_rule
        )
        member_operation = MemberOperation(recovery_rules=recovery_operation)
        updated_member = self.client.update_member(member, [member_operation])
        return updated_member.ByteSize() != 0

    def use_default_recovery_rule(self):
        return self.client.use_default_recovery_rule()

    def get_default_agent(self):
        return self.client.get_default_agent()

    def authorize_recovery(
        self, authorization: MemberRecoveryOperation.Authorization
    ):
        return self.client.authorize_recovery(authorization)

    def remove_non_stored_keys(self):
        stored_keys = self.client.crypto_engine.list_keys()
        stored_proto_keys = [kp.to_key() for kp in stored_keys]
        member = self.client.get_member(self.member_id)
        key_ids_to_remove = []
        for key in member.get_keys():
            if key not in stored_keys:
                key_ids_to_remove.append(key.id)
        if key_ids_to_remove:
            return self.remove_keys(key_ids_to_remove)
        return False

    def get_blob(self, blob_id: str) -> Blob:
        return self.client.get_blob(blob_id)

    def get_token_blob(self, token_id: str, blob_id: str) -> Blob:
        return self.client.get_token_blob(token_id, blob_id)

    def add_address(self, name: str, address: Address) -> AddressRecord:
        return self.client.add_address(name, address)

    def get_address(self, address_id: str) -> AddressRecord:
        return self.client.get_address(address_id)

    def get_addresses(self):
        return self.client.get_addresses()

    def delete_address(self, address_id: str):
        return self.client.delete_address(address_id)

    def create_transfer_token(self, amount: Union[int, float], currency: str):
        return TransferTokenBuilder(self, amount, currency)

    def add_trusted_beneficiary(self, member_id: str) -> bool:
        payload = TrustedBeneficiary.Payload(
            member_id=member_id, nonce=utils.generate_nonce()
        )
        return self.client.add_trusted_beneficiary(payload)

    def remove_trusted_beneficiary(self, member_id: str) -> bool:
        payload = TrustedBeneficiary.Payload(
            member_id=member_id, nonce=utils.generate_nonce()
        )
        return self.client.remove_trusted_beneficiary(payload)

    def get_trusted_beneficiaries(self):
        return self.client.get_trusted_beneficiaries()

    def create_access_token(self, token_payload: TokenPayload) -> Token:
        return self.client.create_access_token(token_payload)

    def create_access_token_for_token_request_id(
        self, token_payload: TokenPayload, token_request_id: str
    ) -> Token:
        return self.client.create_access_token_for_token_request_id(
            token_payload, token_request_id
        )

    def get_access_tokens(self, limit: int, offset: str = None):
        return self.client.get_tokens(
            token_type=GetTokensRequest.ACCESS, offset=offset, limit=limit
        )

    def endorse_token(self, token: Token, key_level: int):
        return self.client.endorse_token(token, key_level)

    def create_customization(
        self, colors=None, display_name=None, logo=None, consent_text=None
    ):
        if colors is None:
            colors = []
        return self.client.create_customization(
            colors, display_name, logo, consent_text
        )
