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


class ErrorResponse(Model):
    """ErrorResponse.

    :param error:
    :type error: ~_restclient.models.RootError
    :param correlation:
    :type correlation: dict[str, str]
    """

    _attribute_map = {
        'error': {'key': 'error', 'type': 'RootError'},
        'correlation': {'key': 'correlation', 'type': '{str}'},
    }

    def __init__(self, error=None, correlation=None):
        super(ErrorResponse, self).__init__()
        self.error = error
        self.correlation = correlation
