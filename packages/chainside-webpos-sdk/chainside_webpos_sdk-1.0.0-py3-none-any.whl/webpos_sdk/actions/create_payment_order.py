"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class CreatePaymentOrderAction(ChainsideAuthenticatedAction):
    route = '/payment-order'
    verb = 'POST'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {}
    route_parameters_schema = {}
    request_body_class = PaymentOrder
    response_body_class = PaymentOrderResponse
    errors = dict(super(ChainsideAuthenticatedAction, ChainsideAuthenticatedAction).errors, **{
        '0001': ValidationErrorException,
    })

    @property
    def payment_order(self):
        return self.request_body

    @payment_order.setter
    def payment_order(self, value):
        self.request_body = value
