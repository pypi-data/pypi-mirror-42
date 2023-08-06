"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject

from .callback_payment_order import CallbackPaymentOrder


class PaymentCancelledCallback(SdkObject):
    schema = {
        "rules": [
            "nullable"
        ],
        "schema": {
            "created_at": {
                "descritpion": "Date in which the callback was sent",
                "rules": [
                    "required"
                ],
                "type": "ISO_8601_date"
            },
            "event": {
                "rules": [
                    "required",
                    "equals:payment.cancelled"
                ],
                "type": "string"
            },
            "object": {
                "rules": [],
                "schema": {
                    "address": {
                        "rules": [
                            "required"
                        ],
                        "type": "base58"
                    },
                    "amount": {
                        "rules": [
                            "decimal",
                            "required"
                        ],
                        "type": "string"
                    },
                    "btc_amount": {
                        "rules": [
                            "required"
                        ],
                        "type": "integer"
                    },
                    "callback_url": {
                        "rules": [
                            "regex[https_url]:^https://",
                            "required"
                        ],
                        "type": "url"
                    },
                    "cancel_url": {
                        "rules": [
                            "regex[https_url]:^https://",
                            "required"
                        ],
                        "type": "url"
                    },
                    "chargeback_date": {
                        "rules": [
                            "required",
                            "nullable"
                        ],
                        "type": "ISO_8601_date"
                    },
                    "continue_url": {
                        "rules": [
                            "regex[https_url]:^https://",
                            "required"
                        ],
                        "type": "url"
                    },
                    "created_at": {
                        "rules": [
                            "required"
                        ],
                        "type": "ISO_8601_date"
                    },
                    "created_by": {
                        "rules": [
                            "required"
                        ],
                        "schema": {
                            "deposit_account": {
                                "rules": [
                                    "required"
                                ],
                                "schema": {
                                    "name": {
                                        "rules": [
                                            "required"
                                        ],
                                        "type": "string"
                                    },
                                    "type": {
                                        "rules": [
                                            "in:bank,bitcoin",
                                            "required"
                                        ],
                                        "type": "string"
                                    },
                                    "uuid": {
                                        "rules": [
                                            "required"
                                        ],
                                        "type": "uuid"
                                    }
                                },
                                "type": "object"
                            },
                            "name": {
                                "rules": [
                                    "required"
                                ],
                                "type": "string"
                            },
                            "type": {
                                "rules": [
                                    "required",
                                    "in:web"
                                ],
                                "type": "string"
                            },
                            "uuid": {
                                "rules": [
                                    "required"
                                ],
                                "type": "uuid"
                            }
                        },
                        "type": "object"
                    },
                    "currency": {
                        "rules": [
                            "required"
                        ],
                        "schema": {
                            "name": {
                                "rules": [
                                    "required"
                                ],
                                "type": "string"
                            },
                            "type": {
                                "rules": [
                                    "in:crypto,fiat",
                                    "required"
                                ],
                                "type": "string"
                            },
                            "uuid": {
                                "rules": [
                                    "required"
                                ],
                                "type": "uuid"
                            }
                        },
                        "type": "object"
                    },
                    "details": {
                        "rules": [
                            "required",
                            "nullable"
                        ],
                        "type": "string"
                    },
                    "dispute_start_date": {
                        "rules": [
                            "required",
                            "nullable"
                        ],
                        "type": "ISO_8601_date"
                    },
                    "expiration_time": {
                        "rules": [
                            "required"
                        ],
                        "type": "ISO_8601_date"
                    },
                    "expires_in": {
                        "rules": [
                            "required"
                        ],
                        "type": "integer"
                    },
                    "rate": {
                        "rules": [
                            "required"
                        ],
                        "schema": {
                            "created_at": {
                                "rules": [
                                    "required"
                                ],
                                "type": "ISO_8601_date"
                            },
                            "source": {
                                "rules": [
                                    "required"
                                ],
                                "type": "string"
                            },
                            "value": {
                                "rules": [
                                    "decimal",
                                    "required"
                                ],
                                "type": "string"
                            }
                        },
                        "type": "object"
                    },
                    "redirect_url": {
                        "rules": [
                            "regex[https_url]:^https://",
                            "required"
                        ],
                        "type": "url"
                    },
                    "reference": {
                        "rules": [
                            "nullable",
                            "required"
                        ],
                        "type": "string"
                    },
                    "required_confirmations": {
                        "rules": [
                            "required"
                        ],
                        "type": "integer"
                    },
                    "resolved_at": {
                        "rules": [
                            "required",
                            "nullable"
                        ],
                        "type": "ISO_8601_date"
                    },
                    "state": {
                        "rules": [
                            "required"
                        ],
                        "schema": {
                            "blockchain_status": {
                                "rules": [
                                    "in:pending,partial,mempool_unconfirmed,unconfirmed,paid,cancelled,expired,network_dispute,mempool_network_dispute,possible_chargeback,chargeback",
                                    "required"
                                ],
                                "type": "string"
                            },
                            "in_confirmation": {
                                "rules": [
                                    "nullable",
                                    "required"
                                ],
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
                            },
                            "paid": {
                                "rules": [
                                    "nullable",
                                    "required"
                                ],
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
                            },
                            "status": {
                                "rules": [
                                    "in:pending,paid,cancelled,expired,network_dispute,chargeback",
                                    "required"
                                ],
                                "type": "string"
                            },
                            "unpaid": {
                                "rules": [
                                    "nullable",
                                    "required"
                                ],
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
                        },
                        "type": "object"
                    },
                    "transactions": {
                        "elements": {
                            "rules": [],
                            "schema": {
                                "blockchain_status": {
                                    "rules": [
                                        "required",
                                        "in:mempool,unconfirmed,confirmed,reverted"
                                    ],
                                    "type": "string"
                                },
                                "created_at": {
                                    "rules": [
                                        "required"
                                    ],
                                    "type": "ISO_8601_date"
                                },
                                "normalized_txid": {
                                    "rules": [
                                        "len:64",
                                        "required"
                                    ],
                                    "type": "string"
                                },
                                "outs": {
                                    "elements": {
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
                                    },
                                    "rules": [
                                        "required"
                                    ],
                                    "type": "array"
                                },
                                "outs_sum": {
                                    "rules": [
                                        "required"
                                    ],
                                    "type": "integer"
                                },
                                "status": {
                                    "rules": [
                                        "required",
                                        "in:unconfirmed,confirmed,reverted"
                                    ],
                                    "type": "string"
                                },
                                "txid": {
                                    "rules": [
                                        "len:64",
                                        "required"
                                    ],
                                    "type": "string"
                                }
                            },
                            "type": "object"
                        },
                        "rules": [
                            "nullable",
                            "required"
                        ],
                        "type": "array"
                    },
                    "uri": {
                        "rules": [
                            "required"
                        ],
                        "type": "string"
                    },
                    "uuid": {
                        "rules": [
                            "required"
                        ],
                        "type": "uuid"
                    }
                },
                "type": "object"
            },
            "object_type": {
                "rules": [
                    "required",
                    "nullable"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {
        'object': CallbackPaymentOrder
    }

    def __init__(self, event, created_at, object_type=None, object=None):
        super().__init__()
        self.event = event
        self.created_at = created_at
        self.object_type = object_type
        self.object = object
