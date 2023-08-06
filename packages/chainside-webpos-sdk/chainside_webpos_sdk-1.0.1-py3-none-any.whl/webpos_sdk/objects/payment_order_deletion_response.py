"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class PaymentOrderResponse(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "cancel_url": {
                "rules": [
                    "regex[https_url]:^https://",
                    "required"
                ],
                "type": "url"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, cancel_url):
        super().__init__()
        self.cancel_url = cancel_url
