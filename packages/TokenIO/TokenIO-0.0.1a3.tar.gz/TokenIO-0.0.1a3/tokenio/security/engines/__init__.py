# -*- coding: utf-8 -*-
from tokenio.proto.security_pb2 import Key
from tokenio.security.keypair import KeyPair


class CryptoEngine:
    def __init__(self, member_id):
        pass

    def generate_key(self, level, expiration_ms=None) -> Key:
        raise NotImplementedError()

    def create_signer(self, level) -> KeyPair:
        raise NotImplementedError()

    def put(self, key_pair: KeyPair) -> KeyPair:
        raise NotImplementedError()

    def get_key_pair_by_level(self, level) -> KeyPair:
        raise NotImplementedError()

    def get_key_pair_by_id(self, key_id) -> KeyPair:
        raise NotImplementedError()

    def list_keys(self):
        key_pairs = [
            KeyPair.generate_key_from_storable_dict(key)
            for key in self._storage.values()
        ]
        return key_pairs

    @classmethod
    def set_active_member_id(cls, member_id):
        raise NotImplementedError()

    @classmethod
    def get_active_member_id(cls):
        raise NotImplementedError()
