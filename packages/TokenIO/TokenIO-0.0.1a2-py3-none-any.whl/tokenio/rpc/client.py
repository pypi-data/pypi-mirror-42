from tokenio.rpc.authenticated_client import AuthenticatedClient
from tokenio.rpc.interceptor.client_authenticator_interceptor import ClientAuthenticatorInterceptor
from tokenio.rpc.unauthenticate_client import UnauthenticatedClient


class Client:
    @staticmethod
    def unauthenticated(channel):
        return UnauthenticatedClient(channel())

    @staticmethod
    def authenticated(channel, member_id, crypto_engine):
        auth_interceptor = ClientAuthenticatorInterceptor(
            member_id, crypto_engine
        )
        auth_channel = channel(auth_interceptor)
        return AuthenticatedClient(member_id, crypto_engine, auth_channel)
