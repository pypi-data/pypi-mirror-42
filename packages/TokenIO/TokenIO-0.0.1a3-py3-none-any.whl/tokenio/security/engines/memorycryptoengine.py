# -*- coding: utf-8 -*-
import time

from tokenio.exceptions import KeyNotFoundError, KeyExpiredError
from tokenio.security.engines import CryptoEngine
from tokenio.security.keypair import KeyPair


class MemoryCryptoEngine(CryptoEngine):
    __active_member_id = ''
    __storage = {}

    def __init__(self, member_id):
        super().__init__(member_id)
        self.member_id = member_id
        MemoryCryptoEngine.set_active_member_id(member_id)

    def generate_key(self, level, expiration_ms=None):
        key_pair = KeyPair.generate_key(level, expiration_ms)
        self.put(key_pair)
        return key_pair.to_key()

    def create_signer(self, level):
        return self.get_key_pair_by_level(level)

    def put(self, key_pair: KeyPair):
        member = self.__storage.get(self.member_id)
        if member is None:
            self.__storage[self.member_id] = {}

        if key_pair.expires_at_ms and key_pair.expires_at_ms < int(
            round(time.time() * 1000)
        ):
            raise KeyExpiredError("Key {} has expired".format(key_pair.id))

        self.__storage[self.member_id][key_pair.level
                                       ] = key_pair.to_storable_dict()
        return self.__storage[self.member_id][key_pair.level]

    def get_key_pair_by_level(self, level):
        member = self.__storage.get(self.member_id)
        if member is None:
            raise KeyNotFoundError(
                'Member {} not found'.format(self.member_id)
            )

        key = member.get(level)
        if key is None:
            raise KeyNotFoundError("No key with level {} found".format(level))

        if key['expires_at_ms'] and key['expires_at_ms'] < int(
            round(time.time() * 1000)
        ):
            raise KeyNotFoundError(
                "Key with level {} has expired".format(level)
            )

        key_pair = KeyPair.generate_key_from_storable_dict(key)
        return key_pair

    def get_key_pair_by_id(self, key_id):
        member = self.__storage.get(self.member_id)
        if member is None:
            raise KeyNotFoundError(
                'Member {} not found'.format(self.member_id)
            )

        for key in member.values():
            if key['id'] == key_id:
                if key['expires_at_ms'] and key['expires_at_ms'] < int(
                    round(time.time() * 1000)
                ):
                    raise KeyNotFoundError(
                        "Key with id {} has expired".format(key_id)
                    )
                return KeyPair.generate_key_from_storable_dict(key)
        raise KeyNotFoundError('No key with id {} found'.format(key_id))

    def list_keys(self):
        member = self.__storage.get(self.member_id)
        if member is None:
            raise KeyNotFoundError(
                'Member {} not found'.format(self.member_id)
            )
        key_pairs = [
            KeyPair.generate_key_from_storable_dict(key)
            for key in member.values()
        ]
        return key_pairs

    @classmethod
    def set_active_member_id(cls, member_id):
        cls.__active_member_id = member_id

    @classmethod
    def get_active_member_id(cls):
        return cls.__active_member_id
