import pytest
from grpc import StatusCode

from tests import utils
from tokenio.exceptions import RequestError
from tokenio.proto.blob_pb2 import Blob
from tokenio.utils import hash_proto_message, generate_nonce


class TestBlob:
    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()
        cls.member = cls.client.create_member(utils.generate_alias())
        cls.other_member = cls.client.create_member(utils.generate_alias())
        cls.file_name = 'file.json'
        cls.file_type = 'application/json'

    def test_create_and_get(self):
        random_data = generate_nonce(100).encode()
        attachment = self.member.create_blob(self.member.member_id, self.file_type, self.file_name, random_data)
        blob_payload = Blob.Payload(owner_id=self.member.member_id, name=self.file_name, type=self.file_type,
                                    data=random_data, access_mode=Blob.DEFAULT)
        blob_hash = hash_proto_message(blob_payload)
        assert attachment.blob_id == "b:{}:{}".format(blob_hash, blob_payload.owner_id.split(':')[-1])
        assert attachment.type == self.file_type
        assert attachment.name == self.file_name

        out_blob = self.member.get_blob(attachment.blob_id)
        assert out_blob.id == attachment.blob_id
        assert out_blob.payload.data == random_data
        assert out_blob.payload.owner_id == self.member.member_id

    def test_empty_data(self):
        random_data = generate_nonce(0).encode()
        attachment = self.member.create_blob(self.member.member_id, self.file_type, self.file_name, random_data)
        out_blob = self.member.get_blob(attachment.blob_id)
        assert out_blob.id == attachment.blob_id
        assert out_blob.payload.data == random_data
        assert out_blob.payload.owner_id == self.member.member_id

    def test_medium_size(self):
        random_data = generate_nonce(5000).encode()
        attachment = self.member.create_blob(self.member.member_id, self.file_type, self.file_name, random_data)
        out_blob = self.member.get_blob(attachment.blob_id)
        assert out_blob.id == attachment.blob_id
        assert out_blob.payload.data == random_data
        assert out_blob.payload.owner_id == self.member.member_id

    def test_public_access(self):
        random_data = generate_nonce(50).encode()
        attachment = self.member.create_blob(self.member.member_id, self.file_type, self.file_name, random_data, Blob.PUBLIC)
        out_blob = self.other_member.get_blob(attachment.blob_id)
        assert out_blob.payload.owner_id == self.member.member_id

    def test_default_access(self):
        random_data = generate_nonce(50).encode()
        attachment = self.member.create_blob(self.member.member_id, self.file_type, self.file_name, random_data, Blob.DEFAULT)
        with pytest.raises(RequestError) as exec_info:
            self.other_member.get_blob(attachment.blob_id)
        assert exec_info.value.details == "BlobId: {}".format(attachment.blob_id)
        assert exec_info.value.code == StatusCode.NOT_FOUND
