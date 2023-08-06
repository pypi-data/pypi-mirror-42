# -*- coding: utf-8 -*-
from tokenio import utils
from tokenio.proto.gateway.gateway_pb2 import *
from tokenio.proto.member_pb2 import MemberUpdate, RecoveryRule, MemberRecoveryRulesOperation, MemberOperation, \
    TrustedBeneficiary
from tokenio.proto.security_pb2 import Key, Signature
from tokenio.proto.token_pb2 import TokenRequestStatePayload, TokenMember, TokenPayload
from tokenio.rpc.authentication_context import AuthenticationContext
from tokenio.security.engines import CryptoEngine


class AuthenticatedClient:
    def __init__(self, member_id, crypto_engine: CryptoEngine, channel):
        self.member_id = member_id
        self.crypto_engine = crypto_engine
        self._channel = channel
        self.on_behalf_of = None
        self.customer_initiated = False

    def __set_on_behalf_of(self):
        if self.on_behalf_of is not None:
            AuthenticationContext.set_on_behalf_of(self.on_behalf_of)
            AuthenticationContext.set_customer_initiated(
                self.customer_initiated
            )

    def __set_request_signer_key_level(self, key_level):
        AuthenticationContext.set_key_level(key_level)

    def get_aliases(self):
        request = GetAliasesRequest()
        with self._channel as channel:
            response = channel.stub.GetAliases(request)
        return response.aliases

    def get_member(self, member_id):
        request = GetMemberRequest(member_id=member_id)
        with self._channel as channel:
            response = channel.stub.GetMember(request)
        return response.member

    def get_account(self, account_id):
        self.__set_on_behalf_of()

        request = GetAccountRequest(account_id=account_id)
        with self._channel as channel:
            response = channel.stub.GetAccount(request)
        return response.account

    def get_accounts(self):
        self.__set_on_behalf_of()
        request = GetAccountsRequest()
        with self._channel as channel:
            response = channel.stub.GetAccounts(request)
        return response.accounts

    def update_member(self, member, operations, metadata=None):
        signer = self.crypto_engine.create_signer(Key.PRIVILEGED)
        member_update = MemberUpdate(
            member_id=member.id,
            prev_hash=member.last_hash,
            operations=operations
        )
        signature = Signature(
            member_id=member.id,
            key_id=signer.id,
            signature=signer.sign_proto_message(member_update)
        )

        if metadata is None:
            metadata = []
        request = UpdateMemberRequest(
            update=member_update,
            update_signature=signature,
            metadata=metadata
        )

        with self._channel as channel:
            response = channel.stub.UpdateMember(request)
        return response.member

    def get_balance(self, account_id, key_level):
        self.__set_on_behalf_of()
        self.__set_request_signer_key_level(key_level)

        request = GetBalanceRequest(account_id=account_id)
        with self._channel as channel:
            response = channel.stub.GetBalance(request)
        # TODO: Error
        return response.balance

    def get_balances(self, account_ids, key_level):
        self.__set_on_behalf_of()
        self.__set_request_signer_key_level(key_level)

        request = GetBalancesRequest(account_id=account_ids)
        with self._channel as channel:
            response = channel.stub.GetBalances(request)
        # TODO: for-loop here?
        return response.response

    def get_transaction(self, account_id, transaction_id, key_level):
        self.__set_on_behalf_of()
        self.__set_request_signer_key_level(key_level)

        request = GetTransactionRequest(
            account_id=account_id, transaction_id=transaction_id
        )

        with self._channel as channel:
            response = channel.stub.GetTransaction(request)
        # TODO: Error
        return response.transaction

    def _page_builder(self, limit, offset=None):
        page = Page(limit=limit)
        if offset is not None:
            page.offset = offset
        return page

    def get_transactions(self, account_id, key_level, limit, offset=None):
        # TODO: offset = None?
        self.__set_on_behalf_of()
        self.__set_request_signer_key_level(key_level)

        request = GetTransactionsRequest(
            account_id=account_id, page=self._page_builder(offset, limit)
        )

        with self._channel as channel:
            response = channel.stub.GetTransactions(request)
        # TODO: Error
        return response.transactions

    def get_token(self, token_id):
        request = GetTokenRequest(token_id=token_id)
        with self._channel as channel:
            response = channel.stub.GetToken(request)
        return response.token

    def get_active_access_token(self, to_member_id):
        request = GetActiveAccessTokenRequest(to_member_id=to_member_id)
        with self._channel as channel:
            response = channel.stub.GetActiveAccessToken(request)
        return response.token

    def use_access_token(self, access_token_id, customer_initiated=False):
        self.on_behalf_of = access_token_id
        self.customer_initiated = customer_initiated

    def clear_access_token(self):
        self.on_behalf_of = None
        self.customer_initiated = False

    def store_token_request(
        self, payload, options, user_ref_id='', customization_id=''
    ):
        request = StoreTokenRequestRequest(
            payload=payload,
            options=options,
            user_ref_id=user_ref_id,
            customization_id=customization_id
        )
        with self._channel as channel:
            response = channel.stub.StoreTokenRequest(request)
        return response.token_request.id

    def create_blob(self, payload):
        request = CreateBlobRequest(payload=payload)
        with self._channel as channel:
            response = channel.stub.CreateBlob(request)
        return response.blob_id

    def get_transfer(self, transfer_id):
        request = GetTransferRequest(transfer_id=transfer_id)
        with self._channel as channel:
            response = channel.stub.GetTransaction(request)
        return response.transfer

    def get_transfers(self, limit, offset=None, token_id=None):
        request = GetTransfersRequest(page=self._page_builder(limit, offset))
        if token_id is not None:
            transfer_filter = GetTransfersRequest.TransferFilter(
                token_id=token_id
            )
            request.filter.CopyFrom(transfer_filter)
        with self._channel as channel:
            response = channel.stub.GetTransfers(request)
        return response

    def create_transfer(self, payload):
        signer = self.crypto_engine.create_signer(Key.LOW)
        payload_signature = Signature(
            member_id=self.member_id,
            key_id=signer.id,
            signature=signer.sign_proto_message(payload)
        )
        request = CreateTransferRequest(
            payload=payload, payload_signature=payload_signature
        )
        with self._channel as channel:
            response = channel.stub.CreateTransfer(request)
        return response.transfer

    def _token_action_from_token(self, token, action):
        return self._token_action(token.payload, action)

    def _token_action(self, payload, action):
        return '{}.{}'.format(
            utils.proto_message_to_bytes(payload).decode(), action
        )

    def cancel_token(self, token):
        signer = self.crypto_engine.create_signer(Key.LOW)
        signature = Signature(
            member_id=self.member_id,
            key_id=signer.id,
            signature=signer.sign(
                self._token_action_from_token(token, 'cancelled').encode()
            )
        )
        request = CancelTokenRequest(token_id=token.id, signature=signature)
        with self._channel as channel:
            response = channel.stub.CancelToken(request)
        return response.result

    def sign_token_request_state(self, token_request_id, token_id, state):
        request_state = TokenRequestStatePayload(
            token_id=token_id, state=state
        )
        request = SignTokenRequestStateRequest(
            payload=request_state, token_request_id=token_request_id
        )
        with self._channel as channel:
            response = channel.stub.SignTokenRequestState(request)
        return response.signature

    def delete_member(self):
        self.__set_on_behalf_of()
        self.__set_request_signer_key_level(Key.PRIVILEGED)
        request = DeleteMemberRequest()
        with self._channel as channel:
            response = channel.stub.DeleteMember(request)
        return response  # TODO: Bool?

    def set_profile(self, profile):
        request = SetProfileRequest(profile=profile)
        with self._channel as channel:
            response = channel.stub.SetProfile(request)
        return response.profile

    def get_profile(self, member_id):
        request = GetProfileRequest(member_id=member_id)
        with self._channel as channel:
            response = channel.stub.GetProfile(request)
        return response.profile

    def set_profile_picture(self, payload):
        request = SetProfilePictureRequest(payload=payload)
        with self._channel as channel:
            response = channel.stub.SetProfilePicture(request)
        return response  # zero byte

    def get_profile_picture(self, member_id, size):
        request = GetProfilePictureRequest(member_id=member_id, size=size)
        with self._channel as channel:
            response = channel.stub.GetProfilePicture(request)
        return response.blob

    def verify_alias(self, verification_id, code):
        request = VerifyAliasRequest(
            verification_id=verification_id, code=code
        )
        with self._channel as channel:
            response = channel.stub.VerifyAlias(request)
        return response  # TODO: Bool?

    def retry_verification(self, alias):
        request = RetryVerificationRequest(alias, member_id=self.member_id)
        with self._channel as channel:
            response = channel.stub.RetryVerification(request)
        return response.verification_id

    def use_default_recovery_rule(self):
        signer = self.crypto_engine.create_signer(Key.PRIVILEGED)
        member = self.get_member(self.member_id)

        default_agent_request = GetDefaultAgentRequest()
        with self._channel as channel:
            default_agent_response = channel.stub.GetDefaultAgent(
                default_agent_request
            )
        rule = RecoveryRule(primary_agent=default_agent_response.member_id)
        recovery_rule_operation = MemberRecoveryRulesOperation(
            recovery_rule=rule
        )

        operation = MemberOperation(recovery_rules=recovery_rule_operation)

        member_update = MemberUpdate(
            member_id=member.id,
            prev_hash=member.last_hash,
            operations=[operation]
        )
        signature = Signature(
            key_id=signer.id,
            member_id=member.id,
            signature=signer.sign_proto_message(member_update)
        )

        request = UpdateMemberRequest(
            update=member_update, update_signature=signature
        )
        with self._channel as channel:
            response = channel.stub.UpdateMember(request)
        return response  # check

    def get_default_agent(self):
        request = GetDefaultAgentRequest()
        with self._channel as channel:
            response = channel.stub.GetDefaultAgent(request)
        return response.member_id

    def authorize_recovery(self, authorization):
        signer = self.crypto_engine.create_signer(Key.PRIVILEGED)
        signature = Signature(
            key_id=signer.id,
            member_id=self.member_id,
            signature=signer.sign_proto_message(authorization)
        )
        return signature

    def get_blob(self, blob_id):
        request = GetBlobRequest(blob_id=blob_id)
        with self._channel as channel:
            response = channel.stub.GetBlob(request)
        return response.blob

    def get_token_blob(self, token_id, blob_id):
        # raise error
        request = GetTokenBlobRequest(token_id=token_id, blob_id=blob_id)
        with self._channel as channel:
            response = channel.stub.GetTokenBlob(request)
        return response.blob

    def add_address(self, name, address):
        signer = self.crypto_engine.create_signer(Key.LOW)
        signature = Signature(
            key_id=signer.id,
            member_id=self.member_id,
            signature=signer.sign_proto_message(address)
        )

        request = AddAddressRequest(
            name=name, address=address, address_signature=signature
        )
        with self._channel as channel:
            response = channel.stub.AddAddress(request)
        return response.address

    def get_address(self, address_id):
        request = GetAddressRequest(address_id=address_id)
        with self._channel as channel:
            response = channel.stub.GetAddress(request)
        return response.address  # TODO: check

    def get_addresses(self):
        request = GetAddressesRequest()
        with self._channel as channel:
            response = channel.stub.GetAddresses(request)
        return response.addresses

    def delete_address(self, address_id):
        request = DeleteAddressRequest(address_id=address_id)
        with self._channel as channel:
            response = channel.stub.DeleteAddress(request)
        return response  # TODO: check

    def get_bank_info(self, bank_id):
        request = GetBankInfoRequest(bank_id=bank_id)
        with self._channel as channel:
            response = channel.stub.GetBankInfo(request)
        return response.info

    def add_trusted_beneficiary(self, payload):
        signer = self.crypto_engine.create_signer(Key.STANDARD)
        signature = Signature(
            key_id=signer.id,
            member_id=self.member_id,
            signature=signer.sign_proto_message(payload)
        )
        trusted_beneficiary = TrustedBeneficiary(
            payload=payload, signature=signature
        )
        request = AddTrustedBeneficiaryRequest(
            trusted_beneficiary=trusted_beneficiary
        )
        with self._channel as channel:
            response = channel.stub.AddTrustedBeneficiary(request)
        return response  # TODO: check

    def remove_trusted_beneficiary(self, payload):
        signer = self.crypto_engine.create_signer(Key.STANDARD)
        signature = Signature(
            key_id=signer.id,
            member_id=self.member_id,
            signature=signer.sign_proto_message(payload)
        )
        trusted_beneficiary = TrustedBeneficiary(
            payload=payload, signature=signature
        )
        request = RemoveTrustedBeneficiaryRequest(
            trusted_beneficiary=trusted_beneficiary
        )
        with self._channel as channel:
            response = channel.stub.RemoveTrustedBeneficiary(request)
        return response  # TODO: check

    def get_trusted_beneficiaries(self):
        request = GetTrustedBeneficiariesRequest()
        with self._channel as channel:
            response = channel.stub.GetTrustedBeneficiaries(request)
        return response.trusted_beneficiaries

    def create_access_token(self, token_payload: TokenPayload):
        token_member = TokenMember(id=self.member_id)
        payload_from = getattr(
            token_payload, 'from'
        )  # `from` is a reserved keyword
        payload_from.CopyFrom(token_member)

        request = CreateAccessTokenRequest(payload=token_payload)
        with self._channel as channel:
            response = channel.stub.CreateAccessToken(request)
        return response.token

    def create_access_token_for_token_request_id(
        self, token_payload, token_request_id
    ):
        request = CreateAccessTokenRequest(
            payload=token_payload, token_request_id=token_request_id
        )
        with self._channel as channel:
            response = channel.stub.CreateAccessToken(request)
        return response.token

    def endorse_token(self, token, key_level):
        signer = self.crypto_engine.create_signer(key_level)
        signature = Signature(
            key_id=signer.id,
            member_id=self.member_id,
            signature=signer.sign(
                self._token_action_from_token(token, 'endorsed').encode()
            )
        )

        request = EndorseTokenRequest(token_id=token.id, signature=signature)
        with self._channel as channel:
            response = channel.stub.EndorseToken(request)
        return response.result

    def get_tokens(self, token_type, limit, offset=None):
        request = GetTokensRequest(
            type=token_type, page=self._page_builder(limit, offset)
        )
        with self._channel as channel:
            response = channel.stub.GetTokens(request)
        return response

    def create_customization(
        self, colors, display_name=None, logo=None, consent_text=None
    ):
        request = CreateCustomizationRequest(colors=colors)
        if display_name is not None:
            request.name = display_name
        if logo is not None:
            request.logo = logo
        if consent_text is not None:
            request.consent_text = consent_text
        with self._channel as channel:
            response = channel.stub.CreateCustomization(request)
        return response.customization_id
