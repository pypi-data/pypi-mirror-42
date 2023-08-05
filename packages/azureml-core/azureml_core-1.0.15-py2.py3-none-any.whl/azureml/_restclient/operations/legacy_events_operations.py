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

from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError

from .. import models


class LegacyEventsOperations(object):
    """LegacyEventsOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def list(
            self, subscription_id, resource_group_name, workspace_name, project_name, run_id, filter=None, continuationtoken=None, orderby=None, sortorder=None, top=None, count=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param project_name:
        :type project_name: str
        :param run_id:
        :type run_id: str
        :param filter:
        :type filter: str
        :param continuationtoken:
        :type continuationtoken: str
        :param orderby:
        :type orderby: list[str]
        :param sortorder: Possible values include: 'Asc', 'Desc'
        :type sortorder: str
        :param top:
        :type top: int
        :param count:
        :type count: bool
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedBaseEvent or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedBaseEvent or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.list.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if filter is not None:
            query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
        if continuationtoken is not None:
            query_parameters['$continuationtoken'] = self._serialize.query("continuationtoken", continuationtoken, 'str')
        if orderby is not None:
            query_parameters['$orderby'] = self._serialize.query("orderby", orderby, '[str]', div=',')
        if sortorder is not None:
            query_parameters['$sortorder'] = self._serialize.query("sortorder", sortorder, 'str')
        if top is not None:
            query_parameters['$top'] = self._serialize.query("top", top, 'int')
        if count is not None:
            query_parameters['$count'] = self._serialize.query("count", count, 'bool')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedBaseEvent', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/projects/{projectName}/runs/{runId}/events'}

    def post(
            self, subscription_id, resource_group_name, workspace_name, project_name, run_id, event_message=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param project_name:
        :type project_name: str
        :param run_id:
        :type run_id: str
        :param event_message:
        :type event_message: ~_restclient.models.BaseEvent
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.post.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if event_message is not None:
            body_content = self._serialize.body(event_message, 'BaseEvent')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    post.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/projects/{projectName}/runs/{runId}/events'}
