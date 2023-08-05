# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class OperationBatchStatusResponseItem(Model):
    """Represents the status of an operation that used the batch API.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar operation_url: status of the long running operation for an
     environment
    :vartype operation_url: str
    :ivar status: status of the long running operation for an environment
    :vartype status: str
    """

    _validation = {
        'operation_url': {'readonly': True},
        'status': {'readonly': True},
    }

    _attribute_map = {
        'operation_url': {'key': 'operationUrl', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(OperationBatchStatusResponseItem, self).__init__(**kwargs)
        self.operation_url = None
        self.status = None
