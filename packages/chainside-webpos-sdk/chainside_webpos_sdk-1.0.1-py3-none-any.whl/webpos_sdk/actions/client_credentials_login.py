"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class ClientCredentialsLoginAction(ChainsideAuthenticatingAction):
    route = '/token'
    verb = 'POST'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {}
    route_parameters_schema = {}
    request_body_class = ClientCredentials
    response_body_class = ClientCredentialsLoginResponse
    errors = dict(super(ChainsideAuthenticatingAction, ChainsideAuthenticatingAction).errors, **{
        '1002': InvalidGrantTypeException,
        '1013': InvalidScopeException,
        '1001': UnauthorizedClientException,
    })

    @property
    def client_credentials(self):
        return self.request_body

    @client_credentials.setter
    def client_credentials(self, value):
        self.request_body = value
