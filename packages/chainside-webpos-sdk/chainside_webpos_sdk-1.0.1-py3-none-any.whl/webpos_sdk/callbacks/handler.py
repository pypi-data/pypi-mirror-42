import json
import base64
import hmac
import hashlib

from sdkboil.callbacks import CallbackHandler

from .factory import CallbacksFactory
from ..lib.constants import CHAINSIDE_SIGNATURE_HEADER


class InvalidSignatureHeaderException(Exception):
    pass


class ChainsideCallbacksHandler(CallbackHandler):
    callbacks = CallbacksFactory.mapping

    def _verify(self, headers, raw_body):
        sig = headers.get(CHAINSIDE_SIGNATURE_HEADER)
        if not sig:
            raise InvalidSignatureHeaderException
        vkey = hashlib.sha256(self.context.secret.encode()).digest()
        return sig == base64.b64encode(hmac.new(vkey, raw_body, hashlib.sha512).digest()).decode()

    def _get_callback_namespace(self, raw_body):
        return json.loads(raw_body)['event']
