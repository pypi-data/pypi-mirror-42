"""
Nigiri auto-generated file
"""
from .common import ChainsideAction, ChainsideAuthenticatedAction, ChainsideAuthenticatingAction
from ..objects import *
from ..exceptions import *


class GetWebPosPaymentsAction(ChainsideAuthenticatedAction):
    route = '/pos/web/{pos_uuid}/payment-order'
    verb = 'GET'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "v1"
    }
    query_parameters_schema = {'status': {'description': 'Status of the payment orders to retrieve', 'type': 'string', 'rules': [
        'in:pending,partial,mempool_unconfirmed,unconfirmed,paid,cancelled,expired,network_dispute,mempool_network_dispute,possible_chargeback,chargeback']}}
    route_parameters_schema = {'pos_uuid': {
        'type': 'uuid', 'rules': ['required']}}
    request_body_class = None
    response_body_class = PaymentOrderList
    errors = dict(super(ChainsideAuthenticatedAction, ChainsideAuthenticatedAction).errors, **{
        '3001': NotFoundException,
    })

    @property
    def pos_uuid(self):
        return self.route_parameters['pos_uuid']

    @pos_uuid.setter
    def pos_uuid(self, value):
        self.route_parameters['pos_uuid'] = value

    @property
    def status(self):
        return self.query_parameters['status']

    @status.setter
    def status(self, value):
        self.query_parameters['status'] = value
