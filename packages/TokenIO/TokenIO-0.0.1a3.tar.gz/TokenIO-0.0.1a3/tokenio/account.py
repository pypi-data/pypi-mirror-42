# -*- coding: utf-8 -*-
from tokenio.rpc.authenticated_client import AuthenticatedClient

import tokenio.member


class Account:
    def __init__(
        self, member: 'tokenio.member.Member', account,
        client: AuthenticatedClient
    ):
        self.member = member
        self.account = account
        self.client = client

    # @property
    # def id(self):
    #     return self.account.id

    def get_id(self):
        return self.account.id

    def get_name(self):
        return self.account.name

    def get_is_locked(self):
        return self.account.is_locked

    def get_bank_id(self):
        return self.account.bank_id

    def balance(self, key_level):
        return self.client.get_balances(self.account.id, key_level)

    def current_balance(self, key_level):
        return self.balance(key_level).current

    def available_balance(self, key_level):
        return self.balance(key_level).available

    def transaction(self, transaction_id, key_level):
        return self.client.get_transaction(
            self.account.id, transaction_id, key_level
        )

    def transactions(self, offset: str, limit: int, key_level):
        return self.transactions(offset, limit, key_level)
