from .model import Model

class StrexTransaction(Model):

    def _accepted_params(self):
        return [
            'transactionId',
            'invoiceText',
            'lastModified',
            'merchantId',
            'price',
            'shortNumber',
            'recipient',
            'oneTimePassword',
            'content',
            'serviceCode',
            'created',
            'deliveryMode',
            'statusCode',
            'detailedStatusCode',
            'accountId',
            'billed',
            'resultCode',
            'resultDescription',
            'properties',
            'tags',
        ]
