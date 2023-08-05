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


class JasmineOperations(object):
    """JasmineOperations operations.

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

    def post_remote_run(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parent_run_id, json_definition=None, file=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parent_run_id:
        :type parent_run_id: str
        :param json_definition:
        :type json_definition: str
        :param file:
        :type file: list[object]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunStatus or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunStatus or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.post_remote_run.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentRunId': self._serialize.url("parent_run_id", parent_run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if json_definition is not None:
            query_parameters['json_definition'] = self._serialize.query("json_definition", json_definition, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'multipart/form-data'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct form data
        form_data_content = {
            'file': file,
        }

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send_formdata(
            request, header_parameters, form_data_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunStatus', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    post_remote_run.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentRunId}/startRun'}

    def post_remote_snapshot_run(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parent_run_id, json_definition=None, snapshot_id=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parent_run_id:
        :type parent_run_id: str
        :param json_definition:
        :type json_definition: str
        :param snapshot_id:
        :type snapshot_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunStatus or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunStatus or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.post_remote_snapshot_run.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentRunId': self._serialize.url("parent_run_id", parent_run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if snapshot_id is not None:
            query_parameters['snapshotId'] = self._serialize.query("snapshot_id", snapshot_id, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/x-www-form-urlencoded'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct form data
        form_data_content = {
            'json_definition': json_definition,
        }

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send_formdata(
            request, header_parameters, form_data_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('RunStatus', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    post_remote_snapshot_run.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentRunId}/startSnapshotRun'}

    def continue_run(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parentrun_id, updated_iterations=None, updated_time=None, updated_exit_score=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parentrun_id:
        :type parentrun_id: str
        :param updated_iterations:
        :type updated_iterations: int
        :param updated_time:
        :type updated_time: int
        :param updated_exit_score:
        :type updated_exit_score: float
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
        url = self.continue_run.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentrunId': self._serialize.url("parentrun_id", parentrun_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if updated_iterations is not None:
            query_parameters['updatedIterations'] = self._serialize.query("updated_iterations", updated_iterations, 'int')
        if updated_time is not None:
            query_parameters['updatedTime'] = self._serialize.query("updated_time", updated_time, 'int')
        if updated_exit_score is not None:
            query_parameters['updatedExitScore'] = self._serialize.query("updated_exit_score", updated_exit_score, 'float')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    continue_run.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentrunId}/continueRun'}

    def continue_run_legacy(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parentrun_id, updated_iterations, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parentrun_id:
        :type parentrun_id: str
        :param updated_iterations:
        :type updated_iterations: int
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
        url = self.continue_run_legacy.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentrunId': self._serialize.url("parentrun_id", parentrun_id, 'str'),
            'updatedIterations': self._serialize.url("updated_iterations", updated_iterations, 'int')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    continue_run_legacy.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentrunId}/continueRun/{updatedIterations}'}

    def create_parent_run(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, create_parent_run_dto=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param create_parent_run_dto:
        :type create_parent_run_dto: ~_restclient.models.CreateParentRunDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: str or ClientRawResponse if raw=true
        :rtype: str or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.create_parent_run.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
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
        if create_parent_run_dto is not None:
            body_content = self._serialize.body(create_parent_run_dto, 'CreateParentRunDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('str', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create_parent_run.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/run'}

    def get_next_pipeline(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parent_run_id, iteration_number, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parent_run_id:
        :type parent_run_id: str
        :param iteration_number:
        :type iteration_number: int
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: JOSNextPipelineDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.JOSNextPipelineDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_next_pipeline.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentRunId': self._serialize.url("parent_run_id", parent_run_id, 'str'),
            'iterationNumber': self._serialize.url("iteration_number", iteration_number, 'int')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('JOSNextPipelineDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_next_pipeline.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentRunId}/iteration/{iterationNumber}'}

    def get_pipeline(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parent_run_id, worker_id, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parent_run_id:
        :type parent_run_id: str
        :param worker_id:
        :type worker_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PipelineDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PipelineDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_pipeline.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentRunId': self._serialize.url("parent_run_id", parent_run_id, 'str'),
            'workerId': self._serialize.url("worker_id", worker_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PipelineDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_pipeline.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentRunId}/workers/{workerId}'}

    def parent_run_status(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, parent_run_id, target_status, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param parent_run_id:
        :type parent_run_id: str
        :param target_status:
        :type target_status: str
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
        url = self.parent_run_status.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'parentRunId': self._serialize.url("parent_run_id", parent_run_id, 'str'),
            'targetStatus': self._serialize.url("target_status", target_status, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    parent_run_status.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/runs/{parentRunId}/status/{targetStatus}'}

    def cancel_child_run(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id:
        :type subscription_id: str
        :param resource_group_name:
        :type resource_group_name: str
        :param workspace_name:
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
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
        url = self.cancel_child_run.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    cancel_child_run.metadata = {'url': '/jasmine/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiment/{experimentName}/cancel/{runId}'}
