# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Manages AML Containers."""

import json
import requests
import os
import uuid

from .image import Image, ImageConfig, Asset, TargetRuntime
from azureml.exceptions import WebserviceException

from azureml._model_management._constants import SUPPORTED_RUNTIMES
from azureml._model_management._constants import UNDOCUMENTED_RUNTIMES
from azureml._model_management._constants import WORKSPACE_RP_API_VERSION
from azureml._model_management._constants import DOCKER_IMAGE_TYPE, WEBAPI_IMAGE_FLAVOR
from azureml._model_management._constants import ARCHITECTURE_AMD64
from azureml._model_management._util import add_sdk_to_requirements
from azureml._model_management._util import upload_dependency
from azureml._model_management._util import wrap_execution_script
from azureml._model_management._util import get_docker_client
from azureml._model_management._util import pull_docker_image
from azureml._model_management._util import start_docker_container
from azureml._model_management._util import get_docker_port
from azureml._model_management._util import container_health_check
from azureml._model_management._util import container_scoring_call
from azureml._model_management._util import cleanup_container
from azureml._model_management._util import validate_path_exists_or_throw


class ContainerImage(Image):
    """
    Class for container images, currently only for Docker images.

    The image contains the dependencies needed to run the model including:

    * The runtime
    * Python environment definitions specified in a Conda file
    * Ability to enable GPU support
    * Custom Docker file for specific run commands

    .. remarks::
        A ContainerImage is retrieved using the :class:`azureml.core.image.image.Image` class constructor
        by passing the name or id of a previously created ContainerImage. The following code example
        shows an image retrieval from a Workspace by both name and id.

        .. code-block:: python

            container_image_from_name = Image(workspace, name="image-name")
            container_image_from_id = Image(workspace, id="image-id")

        To create a new image for use in deployment, build a
        :class:`azureml.core.image.container.ContainerImageConfig` object as shown in the following code example:

        .. code-block:: python

            from azureml.core.image import ContainerImage

            image_config = ContainerImage.image_configuration(execution_script="score.py",
                                                             runtime="python",
                                                             conda_file="myenv.yml",
                                                             description="image for model",
                                                             enable_gpu=True
                                                             )

        See https://docs.microsoft.com/azure/machine-learning/service/tutorial-deploy-models-with-aml#make-script
        for an example of creating both an execution_script and a conda_file.

    """

    _image_type = DOCKER_IMAGE_TYPE
    _image_flavor = WEBAPI_IMAGE_FLAVOR

    _expected_payload_keys = Image._expected_payload_keys + ['assets', 'driverProgram', 'targetRuntime']

    _log_aml_debug = True

    def _initialize(self, workspace, obj_dict):
        """Initialize the ContainerImage object.

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        :raises: None
        """
        super(ContainerImage, self)._initialize(workspace, obj_dict)

        self.image_flavor = ContainerImage._image_flavor
        self.assets = [Asset.deserialize(asset_payload) for asset_payload in obj_dict['assets']]
        self.driver_program = obj_dict['driverProgram']
        self.target_runtime = TargetRuntime.deserialize(obj_dict['targetRuntime'])

    @staticmethod
    def image_configuration(execution_script, runtime, conda_file=None, docker_file=None, schema_file=None,
                            dependencies=None, enable_gpu=None, tags=None, properties=None, description=None):
        """
        Create and return a :class:`azureml.core.image.container.ContainerImageConfig` object.

        This function accepts parameters to define how your model should run within the Webservice, as well as
        the specific environment and dependencies it needs to be able to run.

        :param execution_script: Path to local Python file that contains the code to run for the image. Must
            include both init() and run(input_data) functions that define the model execution steps for
            the Webservice.
        :type execution_script: str
        :param runtime: The runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'.
        :type runtime: str
        :param conda_file: Path to local .yml file containing a Conda environment definition to use for the image.
        :type conda_file: str
        :param docker_file: Path to local file containing additional Docker steps to run when setting up the image.
        :type docker_file: str
        :param schema_file: Path to local file containing a webservice schema to use when the image is deployed.
            Used for generating Swagger specs for a model deployment.
        :type schema_file: str
        :param dependencies: List of paths to additional files/folders that the image needs to run.
        :type dependencies: :class:`list[str]`
        :param enable_gpu: Whether or not to enable GPU support in the image. The GPU image must be used on
            Microsoft Azure Services such as Azure Container Instances, Azure Machine Learning Compute,
            Azure Virtual Machines, and Azure Kubernetes Service.
        :type enable_gpu: bool
        :param tags: Dictionary of key value tags to give this image.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this image. These properties cannot
            be changed after deployment, however new key value pairs can be added.
        :type properties: dict[str, str]
        :param description: A text description to give this image.
        :type description: str
        :return: A configuration object to use when creating the image.
        :rtype: azureml.core.image.container.ContainerImageConfig
        :raises: azureml.exceptions.WebserviceException
        """
        conf = ContainerImageConfig(execution_script, runtime, conda_file, docker_file, schema_file, dependencies,
                                    enable_gpu, tags, properties, description)

        return conf

    def run(self, input_data):
        """
        Run the image locally with the given input data.

        Must have Docker installed and running to work. This method will only work on CPU, as the GPU-enabled image
        can only run on Microsoft Azure Services.

        :param input_data: The input data to pass to the image when run
        :type input_data: varies
        :return: The results of running the image.
        :rtype: varies
        :raises: azureml.exceptions.WebserviceException
        """
        if not input_data:
            raise WebserviceException('Error: You must provide input data.')

        keys_endpoint = 'https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/' \
                        'Microsoft.MachineLearningServices/workspaces/' \
                        '{}/listKeys'.format(self.workspace.subscription_id,
                                             self.workspace.resource_group,
                                             self.workspace.name)
        headers = self.workspace._auth.get_authentication_header()
        params = {'api-version': WORKSPACE_RP_API_VERSION}
        try:
            keys_resp = requests.post(keys_endpoint, headers=headers, params=params)
            keys_resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Unable to retrieve workspace keys to run image:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(keys_resp.status_code, keys_resp.headers,
                                                           keys_resp.content))
        content = keys_resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        keys_dict = json.loads(content)
        try:
            username = keys_dict['containerRegistryCredentials']['username']
            passwords = keys_dict['containerRegistryCredentials']['passwords']
            password = passwords[0]['value']
        except KeyError:
            raise WebserviceException('Unable to retrieve workspace keys to run image, response '
                                      'payload missing container registry credentials.')

        client = get_docker_client(username, password, self.image_location)

        pull_docker_image(client, self.image_location, username, password)

        container_name = self.id + str(uuid.uuid4())[:8]
        container = start_docker_container(client, self.image_location, container_name)

        docker_port = get_docker_port(client, container_name, container)

        docker_url = container_health_check(docker_port, container)

        scoring_result = container_scoring_call(docker_port, input_data, container, docker_url)

        cleanup_container(container)
        return scoring_result

    def serialize(self):
        """Convert this ContainerImage into a json serialized dictionary.

        :return: The json representation of this Image
        :rtype: dict
        """
        serialized_image = super(ContainerImage, self).serialize()
        serialized_image['assets'] = [asset.serialize() for asset in self.assets] if self.assets else None
        serialized_image['driverProgram'] = self.driver_program
        serialized_image['targetRuntime'] = self.target_runtime.serialize() if self.target_runtime else None
        return serialized_image


class ContainerImageConfig(ImageConfig):
    """
    Image config specific to Container deployments - requires execution script and runtime.

    :param execution_script: Path to local file that contains the code to run for the image
    :type execution_script: str
    :param runtime: Which runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'
    :type runtime: str
    :param conda_file: Path to local file containing a conda environment definition to use for the image
    :type conda_file: str
    :param docker_file: Path to local file containing additional Docker steps to run when setting up the image
    :type docker_file: str
    :param schema_file: Path to local file containing a webservice schema to use when the image is deployed
    :type schema_file: str
    :param dependencies: List of paths to additional files/folders that the image needs to run
    :type dependencies: :class:`list[str]`
    :param enable_gpu: Whether or not to enable GPU support in the image. The GPU image must be used on Microsoft
        Azure Services only such as ACI, AML Compute, Azure VMs, and AKS.
    :type enable_gpu: bool
    :param tags: Dictionary of key value tags to give this image
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this image. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this image
    :type description: str
    """

    def __init__(self, execution_script, runtime, conda_file=None, docker_file=None, schema_file=None,
                 dependencies=None, enable_gpu=None, tags=None, properties=None, description=None):
        """Initialize the config object.

        :param execution_script: Path to local file that contains the code to run for the image
        :type execution_script: str
        :param runtime: Which runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'
        :type runtime: str
        :param conda_file: Path to local file containing a conda environment definition to use for the image
        :type conda_file: str
        :param docker_file: Path to local file containing additional Docker steps to run when setting up the image
        :type docker_file: str
        :param schema_file: Path to local file containing a webservice schema to use when the image is deployed
        :type schema_file: str
        :param dependencies: List of paths to additional files/folders that the image needs to run
        :type dependencies: :class:`list[str]`
        :param enable_gpu: Whether or not to enable GPU support in the image. The GPU image must be used on Microsoft
            Azure Services only such as ACI, AML Compute, Azure VMs, and AKS.
        :type enable_gpu: bool
        :param tags: Dictionary of key value tags to give this image
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this image. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this image
        :type description: str
        :raises: azureml.exceptions.WebserviceException
        """
        self.execution_script = execution_script
        self.runtime = runtime
        self.conda_file = conda_file
        self.docker_file = docker_file
        self.schema_file = schema_file
        self.dependencies = dependencies
        self.enable_gpu = enable_gpu
        self.tags = tags
        self.properties = properties
        self.description = description

        self.execution_script_path = os.path.abspath(os.path.dirname(self.execution_script))
        self.validate_configuration()

    def build_create_payload(self, workspace, name, model_ids):
        """Build the creation payload for the Container image.

        :param workspace: The workspace object to create the image in
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the image
        :type name: str
        :param model_ids: A list of model IDs to package into the image
        :type model_ids: :class:`list[str]`
        :return: Container image creation payload
        :rtype: dict
        :raises: azureml.exceptions.WebserviceException
        """
        import copy
        from azureml._model_management._util import image_payload_template
        json_payload = copy.deepcopy(image_payload_template)
        json_payload['name'] = name
        json_payload['kvTags'] = self.tags
        json_payload['imageFlavor'] = WEBAPI_IMAGE_FLAVOR
        json_payload['properties'] = self.properties
        json_payload['description'] = self.description
        json_payload['targetRuntime']['runtimeType'] = SUPPORTED_RUNTIMES[self.runtime.lower()]
        json_payload['targetRuntime']['targetArchitecture'] = ARCHITECTURE_AMD64

        if self.enable_gpu:
            json_payload['targetRuntime']['properties']['installCuda'] = self.enable_gpu
        requirements = add_sdk_to_requirements()
        (json_payload['targetRuntime']['properties']['pipRequirements'], _) = \
            upload_dependency(workspace, requirements)
        if self.conda_file:
            conda_file = self.conda_file.rstrip(os.sep)
            (json_payload['targetRuntime']['properties']['condaEnvFile'], _) = \
                upload_dependency(workspace, conda_file)
        if self.docker_file:
            docker_file = self.docker_file.rstrip(os.sep)
            (json_payload['dockerFileUri'], _) = upload_dependency(workspace, docker_file)

        if model_ids:
            json_payload['modelIds'] = model_ids

        if self.schema_file:
            self.schema_file = self.schema_file.rstrip(os.sep)

        self.execution_script = self.execution_script.rstrip(os.sep)

        driver_mime_type = 'application/x-python'
        if not self.dependencies:
            self.dependencies = []
        wrapped_execution_script = wrap_execution_script(self.execution_script, self.schema_file, self.dependencies,
                                                         ContainerImage._log_aml_debug)

        (driver_package_location, _) = upload_dependency(workspace, wrapped_execution_script)
        json_payload['assets'].append({'id': 'driver', 'url': driver_package_location, 'mimeType': driver_mime_type})

        if self.schema_file:
            self.dependencies.append(self.schema_file)

        for dependency in self.dependencies:
            (artifact_url, artifact_id) = upload_dependency(workspace, dependency, create_tar=True)

            new_asset = {'mimeType': 'application/octet-stream',
                         'id': artifact_id,
                         'url': artifact_url,
                         'unpack': True}
            json_payload['assets'].append(new_asset)

        return json_payload

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Will raise a WebserviceException if validation fails.

        :raises: WebserviceException
        """
        # The driver file must be in the current directory
        if not os.getcwd() == self.execution_script_path:
            raise WebserviceException('Unable to use a driver file not in current directory. '
                                      'Please navigate to the location of the driver file and try again.')

        validate_path_exists_or_throw(self.execution_script, "Driver file")

        execution_script_name, execution_script_extension = os.path.splitext(self.execution_script)
        if execution_script_extension != '.py':
            raise WebserviceException('Invalid driver type. Currently only Python drivers are supported.')

        if self.runtime.lower() not in SUPPORTED_RUNTIMES.keys():
            runtimes = '|'.join(x for x in SUPPORTED_RUNTIMES.keys() if x not in UNDOCUMENTED_RUNTIMES)
            raise WebserviceException('Provided runtime not supported. '
                                      'Possible runtimes are: {}'.format(runtimes))

        if self.conda_file:
            validate_path_exists_or_throw(self.conda_file, "Conda file")

        if self.docker_file:
            validate_path_exists_or_throw(self.docker_file, "Docker file")

        if self.dependencies:
            for dependency in self.dependencies:
                validate_path_exists_or_throw(dependency, "Dependency")

        if self.schema_file:
            validate_path_exists_or_throw(self.schema_file, "Schema file")
            schema_file_path = os.path.abspath(os.path.dirname(self.schema_file))
            common_prefix = os.path.commonprefix([self.execution_script_path, schema_file_path])
            if not common_prefix == self.execution_script_path:
                raise WebserviceException('Schema file must be in the same directory as the driver file, '
                                          'or in a subdirectory.')
