import pytest
from grpc import StatusCode

from tests import utils
from tokenio.exceptions import RequestError
from tokenio.utils import generate_nonce


class TestAddress:

    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()

    def test_add_and_get_address(self):
        member = self.client.create_member(utils.generate_alias())
        name = generate_nonce()
        payload = utils.generate_address()
        address = member.add_address(name, payload)
        result = member.get_address(address.id)
        assert name == address.name
        assert payload == address.address
        assert address == result

    def test_create_and_get_addresses(self):
        member = self.client.create_member(utils.generate_alias())
        addresses = {utils.generate_nonce(): utils.generate_address() for _ in range(3)}
        for name, address in addresses.items():
            member.add_address(name, address)
        actual = {address_record.name: address_record.address for address_record in member.get_addresses()}
        assert addresses == actual

    def test_get_addresses_not_found(self):
        member = self.client.create_member()
        addresses = member.get_addresses()
        assert len(addresses) == 0

    def test_get_address_not_found(self):
        fake_address_id = generate_nonce()
        member = self.client.create_member()
        with pytest.raises(RequestError) as exec_info:
            member.get_address(fake_address_id)
        assert exec_info.value.details == "Unable to locate address {}".format(fake_address_id)
        assert exec_info.value.code == StatusCode.NOT_FOUND

    def test_delete_address(self):
        member = self.client.create_member()
        name = generate_nonce()
        payload = utils.generate_address()
        address = member.add_address(name, payload)
        assert len(member.get_addresses()) == 1
        member.delete_address(address.id)
        assert len(member.get_addresses()) == 0
