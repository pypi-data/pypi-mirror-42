# -*- coding: utf-8 -*-
import base64
import hashlib
import time

try:
    import ed25519
except ImportError:
    from pure25519 import ed25519_oop as ed25519

from tokenio import utils
from tokenio.exceptions import BadSignatureError, MissingSigningKeyError
from tokenio.proto.security_pb2 import Key


class KeyPair:
    def __init__(
            self, verifying_key, signing_key=None, level=None, expires_at_ms=None
    ):
        self.verifying_key = verifying_key
        self.signing_key = signing_key
        self.id = _generate_key_id(verifying_key)
        self.level = level
        self.expires_at_ms = expires_at_ms
        self.algorithm = 'ED25519'

    @classmethod
    def generate_key(cls, level, expiration_ms=None):
        signing_key, verifying_key = ed25519.create_keypair()

        expires_at_ms = None
        if expiration_ms:
            expires_at_ms = int(round(time.time() * 1000)) + expiration_ms

        return cls(
            verifying_key=verifying_key,
            signing_key=signing_key,
            level=level,
            expires_at_ms=expires_at_ms
        )

    def sign_proto_message(self, message):
        data = utils.proto_message_to_bytes(message)
        return self.sign(data)

    def sign(self, data: bytes) -> str:
        if self.signing_key is None:
            raise MissingSigningKeyError(
                "KeyPair does not contain signing_key."
            )
        return base64.urlsafe_b64encode(self.signing_key.sign(data)
                                        ).decode().strip('=')

    def verify(self, message: bytes, signature: bytes):
        try:
            return self.verifying_key.verify(signature, message)
        except ed25519.BadSignatureError:
            raise BadSignatureError("Signature verification failed.")

    def to_storable_dict(self):
        return {
            'id': self.id,
            'algorithm': self.algorithm,
            'level': self.level,
            'verifying_key': base64.urlsafe_b64encode(
                self.verifying_key.to_bytes()
            ).decode(),
            'signing_key': base64.urlsafe_b64encode(
                self.signing_key.to_bytes()
            ).decode(),
            'expires_at_ms': self.expires_at_ms
        }

    @classmethod
    def from_public_key(cls, public_key: bytes):
        verifying_key = ed25519.VerifyingKey(public_key)
        return cls(verifying_key=verifying_key)

    @classmethod
    def generate_key_from_storable_dict(cls, data):
        verifying_key = ed25519.VerifyingKey(
            base64.urlsafe_b64decode(data['verifying_key'].encode())
        )
        signing_key = ed25519.SigningKey(
            base64.urlsafe_b64decode(data['signing_key'].encode())
        )
        expires_at_ms = data['expires_at_ms']
        level = data['level']
        return cls(
            verifying_key=verifying_key,
            signing_key=signing_key,
            level=level,
            expires_at_ms=expires_at_ms
        )

    def to_key(self):
        return Key(
            id=self.id,
            level=self.level,
            algorithm=self.algorithm,
            public_key=base64.urlsafe_b64encode(self.verifying_key.to_bytes()
                                                ).decode().strip('=')
        )

    def __repr__(self):
        return "<KeyPair id: {}>".format(self.id)


def _generate_key_id(verifying_key):
    return base64.urlsafe_b64encode(
        hashlib.sha256(verifying_key.to_bytes()).digest()
    ).decode()[:16]
