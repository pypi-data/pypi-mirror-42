from tests import utils
from tokenio.proto.member_pb2 import Profile, ORIGINAL, SMALL


class TestProfile:
    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()
        cls.member = cls.client.create_member(utils.generate_alias())

    def test_set_profile(self):
        in_profile = Profile(display_name_first='Ming', display_name_last='Xiao')
        back_profile = self.member.set_profile(in_profile)
        out_profile = self.member.get_profile(self.member.member_id)
        assert in_profile == back_profile == out_profile

    def test_update_profile(self):
        in_new_profile = Profile(display_name_first='Wang', display_name_last='Lao')
        back_profile = self.member.set_profile(in_new_profile)
        out_profile = self.member.get_profile(self.member.member_id)
        assert in_new_profile == back_profile == out_profile

    def test_read_profile_not_yours(self):
        in_profile = Profile(display_name_first='Ming', display_name_last='Xiao')
        back_profile = self.member.set_profile(in_profile)
        other_member = self.client.create_member(utils.generate_alias())
        out_profile = other_member.get_profile(self.member.member_id)
        assert in_profile == back_profile == out_profile

    def test_get_profile_picture(self):
        with open('./tests/assets/profile.jpeg', 'rb') as f:
            picture = f.read()
        self.member.set_profile_picture('image/jpeg', picture)
        out_blob = self.member.get_profile_picture(self.member.member_id, ORIGINAL)
        assert out_blob.payload.data == picture
        assert out_blob.payload.type == 'image/jpeg'

        out_small_blob = self.member.get_profile_picture(self.member.member_id, SMALL)
        assert out_small_blob.payload.data != picture
        assert out_small_blob.payload.type == 'image/jpeg'

    def test_get_no_profile_picture(self):
        new_member = self.client.create_member(utils.generate_alias())
        blob = new_member.get_profile_picture(new_member.member_id, ORIGINAL)
        assert blob.id == ''
