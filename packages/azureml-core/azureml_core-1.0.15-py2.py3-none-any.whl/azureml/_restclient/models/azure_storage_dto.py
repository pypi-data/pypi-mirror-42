# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AzureStorageDto(Model):
    """AzureStorageDto.

    :param account_name:
    :type account_name: str
    :param container_name:
    :type container_name: str
    :param endpoint:
    :type endpoint: str
    :param protocol:
    :type protocol: str
    :param credential_type: Possible values include: 'None', 'Sas',
     'AccountKey'
    :type credential_type: str or ~_restclient.models.enum
    :param credential:
    :type credential: str
    :param is_sas:
    :type is_sas: bool
    :param account_key:
    :type account_key: str
    :param sas_token:
    :type sas_token: str
    """

    _attribute_map = {
        'account_name': {'key': 'accountName', 'type': 'str'},
        'container_name': {'key': 'containerName', 'type': 'str'},
        'endpoint': {'key': 'endpoint', 'type': 'str'},
        'protocol': {'key': 'protocol', 'type': 'str'},
        'credential_type': {'key': 'credentialType', 'type': 'str'},
        'credential': {'key': 'credential', 'type': 'str'},
        'is_sas': {'key': 'isSas', 'type': 'bool'},
        'account_key': {'key': 'accountKey', 'type': 'str'},
        'sas_token': {'key': 'sasToken', 'type': 'str'},
    }

    def __init__(self, account_name=None, container_name=None, endpoint=None, protocol=None, credential_type=None, credential=None, is_sas=None, account_key=None, sas_token=None):
        super(AzureStorageDto, self).__init__()
        self.account_name = account_name
        self.container_name = container_name
        self.endpoint = endpoint
        self.protocol = protocol
        self.credential_type = credential_type
        self.credential = credential
        self.is_sas = is_sas
        self.account_key = account_key
        self.sas_token = sas_token
