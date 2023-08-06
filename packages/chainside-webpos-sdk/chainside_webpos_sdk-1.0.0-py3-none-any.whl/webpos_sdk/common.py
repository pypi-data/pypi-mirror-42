from .api_context import ChainsideApiContext
from .actions.common import get_token
from .actions.factory import ChainsideFactory


class AuthenticatedClient(object):
    def __init__(self, config):
        self.context = ChainsideApiContext(config)
        self.factory = ChainsideFactory(self.context)

    def login(self):
        get_token(self.context)
