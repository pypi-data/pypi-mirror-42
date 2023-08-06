import pytest
from grpc import StatusCode

from tests import utils
from tokenio.exceptions import RequestError
from tokenio.proto.token_pb2 import TokenMember, AccessBody, TokenPayload
from tokenio.token_request import TokenRequest


class TestTokenRequest:
    TOKEN_URL = 'https://token.io'

    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()

    def test_add_and_get_transfer_token_request(self):
        member = self.client.create_member(utils.generate_alias())
        payload = member.create_transfer_token(10, 'EUR').set_to_member_id(member.member_id).build()
        stored_request = TokenRequest.builder(payload).add_all_options(redirectUrl=self.TOKEN_URL).build()
        request_id = member.store_token_request(stored_request)
        assert request_id

        retrieved_request = self.client.retrieve_token_request(request_id)
        assert stored_request.token_payload == retrieved_request.payload
        assert request_id == retrieved_request.id
        for k, v in stored_request.options.items():
            assert v == retrieved_request.options.get(k)

    def test_add_and_get_access_token_request(self):
        member = self.client.create_member(utils.generate_alias())
        to_member = TokenMember(id=member.member_id)
        resource = AccessBody.Resource(all_addresses=AccessBody.Resource.AllAddresses())
        access = AccessBody(resources=[resource])
        payload = TokenPayload(to=to_member, access=access)
        stored_request = TokenRequest.builder(payload).add_all_options(redirectUrl=self.TOKEN_URL).build()
        request_id = member.store_token_request(stored_request)
        assert request_id

        retrieved_request = self.client.retrieve_token_request(request_id)
        assert stored_request.token_payload == retrieved_request.payload
        assert request_id == retrieved_request.id
        for k, v in stored_request.options.items():
            assert v == retrieved_request.options.get(k)

    def test_add_and_get_token_request_wrong_member(self):
        member1 = self.client.create_member(utils.generate_alias())
        member2 = self.client.create_member(utils.generate_alias())
        payload = member1.create_transfer_token(10, 'EUR').set_to_member_id(member2.member_id).build()
        stored_request = TokenRequest.builder(payload).build()
        with pytest.raises(RequestError) as exec_info:
            member1.store_token_request(stored_request)
        assert exec_info.value.details == "Access denied to member {}".format(member1.member_id)
        assert exec_info.value.code == StatusCode.PERMISSION_DENIED
