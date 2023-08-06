from tests import utils


class TestBankInfo:
    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()
        cls.banks = cls.client.get_banks().banks

    def test_get_banks(self):
        assert len(self.banks) != 0

    def test_get_bank_info(self):
        bank_id = self.banks[0].id
        member = self.client.create_member()
        bank = member.get_bank_info(bank_id)
        assert bank.linking_uri
