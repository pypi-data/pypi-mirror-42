# -*- coding: utf-8 -*-
from tokenio.proto.security_pb2 import Key


# We can make some of the following functions properties
class AuthenticationContext:
    __on_behalf_of = None
    __key_level = Key.LOW
    __customer_initiated = False

    @classmethod
    def get_on_behalf_of(cls):
        return cls.__on_behalf_of

    @classmethod
    def set_on_behalf_of(cls, token_id):
        cls.__on_behalf_of = token_id

    @classmethod
    def get_key_level(cls):
        return cls.__key_level

    @classmethod
    def set_key_level(cls, level):
        cls.__key_level = level

    @classmethod
    def get_customer_initiated(cls):
        return cls.__customer_initiated

    @classmethod
    def set_customer_initiated(cls, flag):
        cls.__customer_initiated = flag

    @classmethod
    def clear_access_token(cls):
        cls.__on_behalf_of = None
        cls.__customer_initiated = False

    @classmethod
    def reset_key_level(cls):
        cls.__key_level = Key.LOW
        return cls.__key_level

    @classmethod
    def clear(cls):
        cls.__on_behalf_of = None
        cls.__customer_initiated = False
