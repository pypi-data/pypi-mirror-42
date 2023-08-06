# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import random
import string

import base58
from google.protobuf.json_format import MessageToDict

from tokenio.exceptions import CryptoKeyNotFoundException
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.member_pb2 import MemberAddKeyOperation, MemberOperation, MemberRecoveryRulesOperation, RecoveryRule, \
    MemberAliasOperation, MemberOperationMetadata, MemberOperationMetadata
from tokenio.security.keypair import KeyPair


def hash_alias(alias):
    if alias.type == Alias.USERNAME:
        return alias.value
    hash_able_alias = proto_message_to_bytes(alias)
    digest = hashlib.sha256(hash_able_alias).digest()
    return base58.b58encode(digest).decode()


def hash_string(data):
    return hashlib.sha256(data.encode()).hexdigest()


def proto_message_to_bytes(message):
    data = MessageToDict(message)
    return dict_to_bytes(data)


def hash_proto_message(message):
    return base58.b58encode(
        hashlib.sha256(message.SerializeToString()).digest()
    ).decode()


def dict_to_bytes(data):
    return json.dumps(
        data, ensure_ascii=False, separators=(',', ':'), sort_keys=True
    ).encode()


def normalize_alias(alias: Alias) -> Alias:
    alias_type = alias.type
    if alias_type == Alias.EMAIL or alias_type == Alias.DOMAIN:
        alias.value = alias.value.strip().lower()
    return alias


def generate_nonce(length=18):
    return ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )


def to_add_key_operations(keys):
    operations = []
    for key in keys:
        add_key_operation = MemberAddKeyOperation(key=key)
        operation = MemberOperation(add_key=add_key_operation)
        operations.append(operation)
    return operations


def create_add_key_member_operation(key):
    member_add_key_operation = MemberAddKeyOperation(key=key)
    operation = MemberOperation(add_key=member_add_key_operation)
    return operation


def create_recovery_agent_operation(agent_id):
    recovery_rule = RecoveryRule(primary_agent=agent_id)
    rules = MemberRecoveryRulesOperation(recovery_rule=recovery_rule)
    operation = MemberOperation(recovery_rules=rules)
    return operation


def create_add_alias_operation(alias):
    alias_operation = MemberAliasOperation(
        alias_hash=hash_alias(alias), realm=alias.realm
    )
    operation = MemberOperation(add_alias=alias_operation)
    return operation


def create_add_alias_operation_metadata(alias):
    alias_metadata = MemberOperationMetadata.AddAliasMetadata(
        alias=alias, alias_hash=hash_alias(alias)
    )
    metadata = MemberOperationMetadata(add_alias_metadata=alias_metadata)
    return metadata


def find_keys(member, signature):
    keys = member.keys
    if len(keys) == 0:
        return None
    signature_key_id = signature.key_id
    for key in keys:
        if key.id == signature_key_id:
            return key
    return None


def verify_signature(member, payload, signature):
    key = find_keys(member, signature)
    if not key:
        raise CryptoKeyNotFoundException(
            "signature key id: {}".format(signature.key_id)
        )

    key_pair = KeyPair.from_public_key(
        base64.urlsafe_b64decode(padding(key.public_key.encode()))
    )
    key_pair.verify(
        proto_message_to_bytes(payload),
        base64.urlsafe_b64decode(padding(signature.signature.encode()))
    )


def padding(data: bytes):
    missing_padding = len(data) % 4
    data += b'=' * (4 - missing_padding)
    return data
