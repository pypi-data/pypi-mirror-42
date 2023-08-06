from sdkboil.actions import Action

from ..lib.hooks import HeadersHook, AuthorizationHook, AuthenticationHook
from ..exceptions import AccessTokenExpiredException
from ..objects import ClientCredentials


class ChainsideAction(Action):
    presend_hooks = [HeadersHook]
    success_hooks = []
    failure_hooks = []
    route = ''
    verb = ''
    query_parameters_schema = {}
    route_parameters_schema = {}
    request_body_class = None
    response_body_class = None
    errors = {'1004': AccessTokenExpiredException}


class ChainsideAuthenticatingAction(ChainsideAction):
    presend_hooks = ChainsideAction.presend_hooks + [AuthenticationHook]


class ChainsideAuthenticatedAction(ChainsideAction):
    presend_hooks = ChainsideAction.presend_hooks + [AuthorizationHook]

    def run(self):
        try:
            return super().run()
        except AccessTokenExpiredException:
            get_token(self.context)
            return self.run()


def get_token(context):
    from .factory import ChainsideFactory
    login_action = ChainsideFactory(context).make("client_credentials_login")
    login_action.client_credentials = ClientCredentials(
        grant_type='client_credentials', scope='*')
    access_token = login_action.run().access_token
    context.cache.set(context.token_cache_key, access_token)
