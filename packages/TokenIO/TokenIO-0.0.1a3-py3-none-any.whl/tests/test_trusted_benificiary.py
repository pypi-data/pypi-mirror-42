from tests import utils


class TestTrustedBenificiary:
    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()
        cls.member1 = cls.client.create_member(utils.generate_alias())
        cls.member2 = cls.client.create_member(utils.generate_alias())
        cls.member3 = cls.client.create_member(utils.generate_alias())

    def test_add_and_get_trusted_beneficiary(self):
        self.member1.add_trusted_beneficiary(self.member2.member_id)
        beneficiaries = self.member1.get_trusted_beneficiaries()
        beneficiary_id = [beneficiary.payload.member_id for beneficiary in beneficiaries]
        assert [self.member2.member_id] == beneficiary_id

        self.member1.add_trusted_beneficiary(self.member3.member_id)
        beneficiaries = self.member1.get_trusted_beneficiaries()
        beneficiary_id = [beneficiary.payload.member_id for beneficiary in beneficiaries]
        assert [self.member2.member_id, self.member3.member_id] == beneficiary_id

    def test_remove_trusted_beneficiary(self):
        self.member2.add_trusted_beneficiary(self.member1.member_id)
        self.member2.add_trusted_beneficiary(self.member3.member_id)
        beneficiaries = self.member2.get_trusted_beneficiaries()
        beneficiary_id = [beneficiary.payload.member_id for beneficiary in beneficiaries]
        assert [self.member1.member_id, self.member3.member_id] == beneficiary_id

        self.member2.remove_trusted_beneficiary(self.member3.member_id)
        beneficiaries = self.member2.get_trusted_beneficiaries()
        beneficiary_id = [beneficiary.payload.member_id for beneficiary in beneficiaries]
        assert [self.member1.member_id] == beneficiary_id

        self.member2.remove_trusted_beneficiary(self.member1.member_id)
        beneficiaries = self.member2.get_trusted_beneficiaries()
        assert len(beneficiaries) == 0
