"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class PaidStatus(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "crypto": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            },
            "fiat": {
                "rules": [
                    "required",
                    "decimal"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, crypto, fiat):
        super().__init__()
        self.crypto = crypto
        self.fiat = fiat
