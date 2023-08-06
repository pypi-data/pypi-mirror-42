"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class ClientCredentials(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "grant_type": {
                "rules": [
                    "equals:client_credentials",
                    "required"
                ],
                "type": "string"
            },
            "scope": {
                "rules": [
                    "in:*",
                    "required"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, scope, grant_type):
        super().__init__()
        self.scope = scope
        self.grant_type = grant_type
