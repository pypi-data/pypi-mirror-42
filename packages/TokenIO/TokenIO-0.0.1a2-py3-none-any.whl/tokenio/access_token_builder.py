# -*- coding: utf-8 -*-
from tokenio import utils
from tokenio.exceptions import IllegalArgumentException
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.token_pb2 import TokenPayload, AccessBody, TokenMember


class AccessTokenBuilder:
    def __init__(self, payload=None):
        self.payload = payload
        if payload is None:
            self.payload = TokenPayload(
                version='1.0',
                ref_id=utils.generate_nonce(),
                access=AccessBody(),
                to=TokenMember()
            )
            payload_from = getattr(self.payload, 'from')
            payload_from.CopyFrom(TokenMember())

    @classmethod
    def create_with_alias(cls, redeemer_alias: Alias):
        return cls().alias_to(redeemer_alias)

    @classmethod
    def create_with_redeemer_id(cls, redeemer_member_id: str):
        return cls().redeemer_to(redeemer_member_id)

    def alias_to(self, redeemer_alias):
        self.payload.to.alias.CopyFrom(redeemer_alias)
        return self

    def redeemer_to(self, redeemer_member_id: str):
        self.payload.to.alias.id = redeemer_member_id
        return self

    @classmethod
    def from_payload(cls, payload: TokenPayload):
        new_payload = TokenPayload()
        new_payload.CopyFrom(payload)
        new_payload.access.CopyFrom(AccessBody())
        new_payload.ref_id = utils.generate_nonce()
        return cls(new_payload)

    def for_all(self):
        return self.for_all_accounts(). \
            for_all_addresses(). \
            for_all_balances(). \
            for_all_transactions(). \
            for_all_transfer_destinations()

    def for_all_addresses(self):
        addresses = AccessBody.Resource.AllAddresses()
        resource = AccessBody.Resource(all_addresses=addresses)
        self.__add_resource(resource)
        return self

    def for_address(self, address_id):
        address = AccessBody.Resource.Address(address_id=address_id)
        resource = AccessBody.Resource(address=address)
        self.__add_resource(resource)
        return self

    def for_all_accounts(self):
        all_accounts = AccessBody.Resource.AllAccounts()
        resource = AccessBody.Resource(all_accounts=all_accounts)
        self.__add_resource(resource)
        return self

    def for_all_accounts_at_bank(self, bank_id):
        all_accounts = AccessBody.Resource.AllAccountsAtBank(bank_id=bank_id)
        resource = AccessBody.Resource(all_accounts_at_bank=all_accounts)
        self.__add_resource(resource)
        return self

    def for_account(self, account_id):
        account = AccessBody.Resource.Account(account_id=account_id)
        resource = AccessBody.Resource(account=account)
        self.__add_resource(resource)
        return self

    def for_all_transactions(self):
        all_transactions = AccessBody.Resource.AllAccountTransactions()
        resource = AccessBody.Resource(all_transactions=all_transactions)
        self.__add_resource(resource)
        return self

    def for_all_transactions_at_bank(self, bank_id):
        all_transactions = AccessBody.Resource.AllTransactionsAtBank(
            bank_id=bank_id
        )
        resource = AccessBody.Resource(
            all_transactions_at_bank=all_transactions
        )
        self.__add_resource(resource)
        return self

    def for_account_transactions(self, account_id):
        account_transactions = AccessBody.Resource.AccountTransactions(
            account_id=account_id
        )
        resource = AccessBody.Resource(transactions=account_transactions)
        self.__add_resource(resource)
        return self

    def for_all_balances(self):
        all_balances = AccessBody.Resource.AllAccountBalances()
        resource = AccessBody.Resource(all_balances=all_balances)
        self.__add_resource(resource)
        return self

    def for_all_balances_at_bank(self, bank_id):
        all_balances = AccessBody.Resource.AllBalancesAtBank(bank_id=bank_id)
        resource = AccessBody.Resource(all_balances_at_bank=all_balances)
        self.__add_resource(resource)
        return self

    def for_account_balances(self, account_id):
        account_balances = AccessBody.Resource.AccountBalance(
            account_id=account_id
        )
        resource = AccessBody.Resource(balances=account_balances)
        self.__add_resource(resource)
        return self

    def for_all_transfer_destinations(self):
        all_destinations = AccessBody.Resource.AllTransferDestinations()
        resource = AccessBody.Resource(
            all_transfer_destinations=all_destinations
        )
        self.__add_resource(resource)
        return self

    def for_all_transfer_destinations_at_bank(self, bank_id):
        bank_destinations = AccessBody.Resource.AllTransferDestinationsAtBank(
            bank_id=bank_id
        )
        resource = AccessBody.Resource(
            all_transfer_destinations_at_bank=bank_destinations
        )
        self.__add_resource(resource)
        return self

    def for_transfer_destinations(self, account_id):
        destinations = AccessBody.Resource.TransferDestinations(
            account_id=account_id
        )
        resource = AccessBody.Resource(transfer_destinations=destinations)
        self.__add_resource(resource)
        return self

    def __add_resource(self, resource):
        self.payload.access.resources.extend([resource])
        return self

    def build(self):
        if len(self.payload.access.resources) == 0:
            raise IllegalArgumentException(
                'At least one access resource must be set'
            )
        return self.payload
