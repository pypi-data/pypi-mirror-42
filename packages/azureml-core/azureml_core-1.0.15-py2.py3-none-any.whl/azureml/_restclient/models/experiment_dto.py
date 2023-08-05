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


class ExperimentDto(Model):
    """ExperimentDto.

    :param experiment_id:
    :type experiment_id: str
    :param name:
    :type name: str
    :param description:
    :type description: str
    :param created_utc:
    :type created_utc: datetime
    """

    _attribute_map = {
        'experiment_id': {'key': 'experimentId', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'created_utc': {'key': 'createdUtc', 'type': 'iso-8601'},
    }

    def __init__(self, experiment_id=None, name=None, description=None, created_utc=None):
        super(ExperimentDto, self).__init__()
        self.experiment_id = experiment_id
        self.name = name
        self.description = description
        self.created_utc = created_utc
