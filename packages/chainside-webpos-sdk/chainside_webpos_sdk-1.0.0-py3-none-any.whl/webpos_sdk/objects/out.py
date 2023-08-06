"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class Out(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "amount": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            },
            "n": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, amount, n):
        super().__init__()
        self.amount = amount
        self.n = n
