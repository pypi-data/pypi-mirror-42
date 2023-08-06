import time
import urllib.parse

import pytest
from grpc import StatusCode

from tests import utils
from tokenio.access_token_builder import AccessTokenBuilder
from tokenio.exceptions import RequestError
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.security_pb2 import Key
from tokenio.token_request import TokenRequest
from tokenio.utils import generate_nonce, proto_message_to_bytes


class TestAccessToken:
    TOKEN_LOOKUP_POLL_FREQUENCY = 1.5

    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()

    def test_get_access_token(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        address = member1.add_address(generate_nonce(), utils.generate_address())
        payload = AccessTokenBuilder.create_with_alias(member1.get_first_alias()).for_address(address.id).build()
        access_token = member1.create_access_token(payload)
        result = member1.get_token(access_token.id)
        assert access_token == result

    def test_get_access_tokens(self):
        # TODO: cleanup
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        member2 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        address = member1.add_address(generate_nonce(), utils.generate_address())
        payload = AccessTokenBuilder.create_with_alias(member1.get_first_alias()).for_address(address.id).build()
        member1.create_access_token(payload)
        payload = AccessTokenBuilder.create_with_alias(member2.get_first_alias()).for_address(address.id).build()
        access_token = member1.create_access_token(payload)
        member1.endorse_token(access_token, Key.STANDARD)
        time.sleep(self.TOKEN_LOOKUP_POLL_FREQUENCY * 2)
        result = member1.get_access_tokens(limit=2, offset=None)
        token_ids = [item.id for item in result.tokens]
        assert access_token.id in token_ids

    def test_only_one_access_token_allowed(self):
        member = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        address = member.add_address(generate_nonce(), utils.generate_address())
        payload = AccessTokenBuilder.create_with_alias(member.get_first_alias()).for_address(address.id).build()
        member.create_access_token(payload)
        payload = AccessTokenBuilder.create_with_alias(member.get_first_alias()).for_address(address.id).build()
        with pytest.raises(RequestError) as exec_info:
            member.create_access_token(payload)
        assert exec_info.value.details == "Token from {} to {} already exists".format(member.member_id,
                                                                                      member.member_id)
        assert exec_info.value.code == StatusCode.ALREADY_EXISTS

    def test_get_access_token_id(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        member2 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        address = member1.add_address(generate_nonce(), utils.generate_address())
        payload = AccessTokenBuilder.create_with_alias(member2.get_first_alias()).for_address(address.id).build()
        request = TokenRequest.builder(payload).build()
        token_request_id = member2.store_token_request(request)
        access_token = member1.create_access_token(payload)
        member1.endorse_token(access_token, Key.STANDARD)
        signature = member1.sign_token_request_state(token_request_id, access_token.id, generate_nonce())
        assert signature.ByteSize != 0
        result = self.client.get_token_request_result(token_request_id)
        assert result.token_id == access_token.id
        assert result.signature.signature == signature.signature

    def test_create_access_token_idempotent(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        address = member1.add_address(generate_nonce(), utils.generate_address())
        payload = AccessTokenBuilder.create_with_alias(member1.get_first_alias()).for_address(address.id).build()
        member1.endorse_token(member1.create_access_token(payload), Key.STANDARD)
        member1.endorse_token(member1.create_access_token(payload), Key.STANDARD)
        time.sleep(self.TOKEN_LOOKUP_POLL_FREQUENCY * 2)
        result = member1.get_access_tokens(2, None)
        assert len(result.tokens) == 1

    def test_auth_flow(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        member2 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        payload = AccessTokenBuilder.create_with_alias(member2.get_first_alias()).for_all().build()

        access_token = member1.create_access_token(payload)
        token = member1.get_token(access_token.id)
        request_id = generate_nonce()
        original_state = generate_nonce()
        csrf_token = generate_nonce()

        token_request_url = self.client.generate_token_request_url(request_id, original_state, csrf_token)
        state = urllib.parse.urlparse(token_request_url).query.split('=')[1]
        signature = member1.sign_token_request_state(request_id, token.id, state)
        path = 'path?tokenId={}&state={}&signature={}'.format(token.id, state,
                                                              urllib.parse.quote(
                                                                  proto_message_to_bytes(signature).decode()))
        token_request_callback_url = 'http://localhost:80/' + path
        callback = self.client.parse_token_request_callback_url(token_request_callback_url, csrf_token)
        assert original_state == callback.state

    def test_request_signature(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        member2 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        payload = AccessTokenBuilder.create_with_alias(member2.get_first_alias()).for_all().build()
        token = member1.create_access_token(payload)
        signature = member1.sign_token_request_state(generate_nonce(), token.id, generate_nonce())
        assert signature.signature

    def test_access_token_builder_set_transfer_destinations(self):
        member1 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        member2 = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        payload = AccessTokenBuilder.create_with_alias(
            member2.get_first_alias()).for_all_transfer_destinations().build()
        access_token = member1.create_access_token(payload)
        result = member1.get_token(access_token.id)
        assert access_token == result
