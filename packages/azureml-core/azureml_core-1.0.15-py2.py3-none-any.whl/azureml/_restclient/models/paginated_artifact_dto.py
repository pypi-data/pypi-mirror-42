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


class PaginatedArtifactDto(Model):
    """PaginatedArtifactDto.

    :param value:
    :type value: list[~_restclient.models.ArtifactDto]
    :param continuation_token:
    :type continuation_token: str
    :param count:
    :type count: int
    """

    _attribute_map = {
        'value': {'key': 'value', 'type': '[ArtifactDto]'},
        'continuation_token': {'key': 'continuationToken', 'type': 'str'},
        'count': {'key': 'count', 'type': 'int'},
    }

    def __init__(self, value=None, continuation_token=None, count=None):
        super(PaginatedArtifactDto, self).__init__()
        self.value = value
        self.continuation_token = continuation_token
        self.count = count
