from tests import utils
from tokenio.proto.alias_pb2 import Alias
from tokenio.proto.member_pb2 import RecoveryRule, MemberRecoveryOperation
from tokenio.proto.security_pb2 import Key


class TestMemberRegistration:
    @classmethod
    def setup_class(cls):
        cls.client = utils.initialize_client()

    def test_create_member(self):
        alias = utils.generate_alias(type=Alias.DOMAIN)  # Alias.EMAIL failed
        member = self.client.create_member(alias)
        keys = member.get_keys()
        assert len(keys) == 3
        assert len(member.get_aliases()) != 0

    def test_create_member_no_alias(self):
        member = self.client.create_member()
        keys = member.get_keys()
        assert len(keys) == 3
        assert len(member.get_aliases()) == 0

    def test_login_member(self):
        alias = utils.generate_alias(type=Alias.DOMAIN)
        member = self.client.create_member(alias)
        logged_in = self.client.get_member(member.member_id)

        expected_aliases = utils.repeated_composite_container_to_list(member.get_aliases())
        actual_aliases = utils.repeated_composite_container_to_list(logged_in.get_aliases())
        assert sorted(expected_aliases) == sorted(actual_aliases)

    def test_add_and_remove_alias(self):
        alias1 = utils.generate_alias(type=Alias.DOMAIN)
        alias2 = utils.generate_alias(type=Alias.DOMAIN)
        member = self.client.create_member(alias1)

        member.add_alias(alias2)
        received_aliases = utils.repeated_composite_container_to_list(member.get_aliases())
        expected_aliases = [alias1, alias2]
        assert sorted(received_aliases, key=lambda v: v.value) == sorted(expected_aliases, key=lambda v: v.value)

        member.remove_alias(alias1)
        received_aliases = utils.repeated_composite_container_to_list(member.get_aliases())
        expected_aliases = [alias2]
        assert received_aliases == expected_aliases

    def test_is_alias_exist(self):
        alias = utils.generate_alias(type=Alias.DOMAIN)
        assert not self.client.is_alias_exists(alias)

        self.client.create_member(alias)
        assert self.client.is_alias_exists(alias)

    def test_recovery(self):
        alias = utils.generate_alias(type=Alias.DOMAIN)
        member = self.client.create_member(alias)
        member.use_default_recovery_rule()
        verification_id = self.client.begin_recovery(alias)
        recovered = self.client.complete_recovery_with_default_rule(member.member_id, verification_id, 'code')
        assert member.member_id == recovered.member_id
        assert len(recovered.get_keys()) == 3
        assert len(recovered.get_aliases()) == 0
        assert not self.client.is_alias_exists(alias)

        recovered.verify_alias(verification_id, 'code')
        assert self.client.is_alias_exists(alias)
        received_aliases = utils.repeated_composite_container_to_list(recovered.get_aliases())
        expected_aliases = [alias]
        assert received_aliases == expected_aliases

    def test_recovery_with_secondary_agent(self):
        alias = utils.generate_alias(type=Alias.DOMAIN)
        member = self.client.create_member(alias)
        primary_agent_id = member.get_default_agent()
        secondary_agent = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))
        unused_secondary_agent = self.client.create_member(utils.generate_alias(type=Alias.DOMAIN))

        recovery_rule = RecoveryRule(primary_agent=primary_agent_id,
                                     secondary_agents=[secondary_agent.member_id, unused_secondary_agent.member_id])

        member.add_recovery_rule(recovery_rule)
        # remove all keys
        self.client.CryptoEngine.__storage = {}
        crypto_engine = self.client.CryptoEngine(member.member_id)
        key = crypto_engine.generate_key(Key.PRIVILEGED)
        verification_id = self.client.begin_recovery(alias)
        authorization = MemberRecoveryOperation.Authorization(member_id=member.member_id,
                                                              prev_hash=member.get_last_hash(),
                                                              member_key=key)

        signature = secondary_agent.authorize_recovery(authorization)
        op1 = self.client.get_recovery_authorization(verification_id, 'code', key)
        op2 = MemberRecoveryOperation(authorization=authorization, agent_signature=signature)
        recovered = self.client.complete_recovery(member.member_id, [op1, op2], key, crypto_engine)

        assert member.member_id == recovered.member_id
        assert len(recovered.get_keys()) == 3
        assert len(recovered.get_aliases()) == 0
        assert not self.client.is_alias_exists(alias)

        recovered.verify_alias(verification_id, 'code')
        assert self.client.is_alias_exists(alias)
        assert [alias] == utils.repeated_composite_container_to_list(recovered.get_aliases())
