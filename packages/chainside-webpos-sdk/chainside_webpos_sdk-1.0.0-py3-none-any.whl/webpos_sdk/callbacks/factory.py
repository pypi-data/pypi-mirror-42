"""
Nigiri auto-generated file
"""

from ..objects import PaymentCompletedCallback
from ..objects import PaymentDisputeStartCallback
from ..objects import PaymentOverpaidCallback
from ..objects import PaymentCancelledCallback
from ..objects import PaymentDisputeEndCallback
from ..objects import PaymentExpiredCallback
from ..objects import PaymentChargebackCallback


class CallbacksFactory(object):
    mapping = {
        'payment.completed': PaymentCompletedCallback,
        'payment.dispute.start': PaymentDisputeStartCallback,
        'payment.overpaid': PaymentOverpaidCallback,
        'payment.cancelled': PaymentCancelledCallback,
        'payment.dispute.end': PaymentDisputeEndCallback,
        'payment.expired': PaymentExpiredCallback,
        'payment.chargeback': PaymentChargebackCallback,
    }
