"""
Nigiri auto-generated file
"""
from .api_context import ChainsideApiContext
from .common import AuthenticatedClient
from .actions.factory import ChainsideFactory
from .lib.cache import CacheAdapterFactory
from .lib.constants import CHAINSIDE_API_HOSTNAME, CHAINSIDE_SANDBOX_API_HOSTAME


class Client(AuthenticatedClient):
    def __init__(self, config):

        super().__init__(config)
        self.login()

    def client_credentials_login(self, client_credentials):
        action = self.factory.make('client_credentials_login')
        action.client_credentials = client_credentials
        return action.run()

    def delete_payment_order(self, payment_order_uuid):
        action = self.factory.make('delete_payment_order')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def get_payment_order(self, payment_order_uuid):
        action = self.factory.make('get_payment_order')
        action.payment_order_uuid = payment_order_uuid
        return action.run()

    def get_web_pos_payments(self, pos_uuid, status=None):
        action = self.factory.make('get_web_pos_payments')
        action.pos_uuid = pos_uuid
        if status:
            action.status = status
        return action.run()

    def create_payment_order(self, payment_order):
        action = self.factory.make('create_payment_order')
        action.payment_order = payment_order
        return action.run()
