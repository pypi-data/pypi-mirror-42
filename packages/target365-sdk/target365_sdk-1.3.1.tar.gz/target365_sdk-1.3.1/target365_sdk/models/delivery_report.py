from .model import Model

class DeliveryReport(Model):

    def _accepted_params(self):
        return [
            'correlationId',
            'transactionId',
            'price',
            'sender',
            'recipient',
            'operator',
            'statusCode',
            'detailedStatusCode',
            'delivered',
            'billed',
        ]
