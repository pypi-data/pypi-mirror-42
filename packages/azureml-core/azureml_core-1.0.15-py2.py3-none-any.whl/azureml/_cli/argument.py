# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import copy


class Argument:
    """ This class defines a parser argument. The fields in this class are exactly similar to
    ArgumentParser.add_argument function, except the function_arg_name and positional_argument.
    function_arg_name denotes the name of the function argument in the CLI command handler function.
    positional_argument is used for registering positional argument with azure.cli."""
    # long_form is the long form name of the option. short_form is the short
    # form name of the option.
    #
    # long_form, short_form are the required arguments.
    # positional_argument=True indicates the argument is a positional argument.
    def __init__(self, function_arg_name, long_form, short_form, help=None, action=None,
                 nargs=None, const=None, default=None, type=None, choices=None,
                 required=False, metavar=None, dest=None, positional_argument=False):
        # We don't support empty long_form argument names.
        assert len(function_arg_name) > 0

        # For az cli and pythonic code, replacing - to _
        function_arg_name = function_arg_name.replace("-", "_")
        assert len(long_form) > 0, "Empty long_form name for an argument is not supported."

        # Checking for - because short form can be empty or doesn't start with -.
        if short_form.startswith("-"):
            assert len(short_form) == 2, "More than one letter short form names are not supported."

        self.function_arg_name = function_arg_name
        self.long_form = long_form
        self.short_form = short_form
        self.help = help
        self.action = action
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.metavar = metavar
        self.dest = dest
        self.positional_argument = positional_argument

    def get_key_based_arguments_as_dict(self):
        """ Returns the key-based arguments as a dictionary while skipping all key-based arguments
        that are None. This function doesn't include positional_argument, as that is not an
        argument in ArgumentParser.add_argument and that is only needed for registering commands
        with azure cli, not with azureml._cli"""
        # TODO: Need to replace it with automatic non none check using inspect.
        dict = {}

        if self.help:
            dict["help"] = self.help

        if self.action:
            dict["action"] = self.action

        if self.nargs:
            dict["nargs"] = self.nargs

        if self.const:
            dict["const"] = self.const

        if self.default:
            dict["default"] = self.default

        if self.type:
            dict["type"] = self.type

        if self.choices:
            dict["choices"] = self.choices

        if self.required:
            dict["required"] = self.required

        if self.metavar:
            dict["metavar"] = self.metavar

        if self.dest:
            dict["dest"] = self.dest
        return dict

    def clone(self):
        return copy.deepcopy(self)

    def get_required_true_copy(self):
        """ Returns a cloned copy of this argument where required=True"""
        local_copy = self.clone()
        local_copy.required = True
        return local_copy

# Some base_sdk_common arguments across many commands are described here, which can be
# imported and directly used. If an option is used more than once, then it should be put here.


# Experiment command options
RUN_CONFIGURATION_OPTION = Argument("run_configuration", "--run-configuration", "-c",
                                    help="Name of the run configuration.")

TARGET_OPTION = Argument("target", "--target", "-t", help="Compute resources used by the run.")

ASYNC_OPTION = Argument("run_async", "--async", "-a", help="Disable output streaming.", action="store_true")

CONDA_DEPENDENCY_OPTION = Argument("conda_dependencies", "--conda-dependencies", "-d",
                                   help="Override the default Conda dependencies file.")

SPARK_DEPENDENCY_OPTION = Argument("spark_dependencies", "--spark-dependencies", "-s",
                                   help="Override the default Spark dependencies file.")

PROJECT_OPTION = Argument("project", "--project", "-p", help="Path to the project.")

UNTRACKED_RUN_OPTION = Argument("untracked", "--untracked", "-u", help="Disable history tracking.",
                                action="store_true")

PREPARE_RUN_OPTION = Argument("prepare", "--prepare", "",
                              help="Override the default autoPrepareEnvironment option in the runconfig to true.",
                              action="store_true")

WAIT_OPTION = Argument("wait", "--wait", "", help="Wait for run finalization.", action="store_true", default=False)

RUN_ID_OPTION = Argument("run_id", "--run", "-r", help="The runId of an experiment run.")


# Project command options
# Options will be by default set to required=False.
PROJECT_NAME = Argument("project_name", "--name", "-n", help="Project name.")

EXPERIMENT_NAME = Argument("experiment_name", "--experiment-name", "", help="Experiment name.")

RESOURCE_GROUP_NAME = Argument("resource_group_name", "--resource-group", "-g", help="Resource group name.")

LOCATION = Argument("location", "--location", "-l", help="Location for resource.")

WORKSPACE_NAME = Argument("workspace_name", "--workspace", "-w", help="Workspace name.")

# Path used in az ml project commands is slightly different than the one used in az ml experiment commands.
PROJECT_PATH = Argument("path", "--path", "", help="Path to a project.")


# Workspace related arguments.

FRIENDLY_NAME = Argument("friendly_name", "--friendly-name", "-f", help="Friendly name.")


# Compute target attach arguments.

ADDRESS = Argument("address", "--address", "-a", help="DNS name or IP address of the target.")

SSH_PORT = Argument("ssh_port", "--ssh-port", "", help="ssh port that can be use to connect to the compute.",
                    default="22")

TARGET_NAME = Argument("name", "--name", "-n", help="Specifies the compute target name. The name should be unique "
                                                    "among all other compute targets in the project.")

PASSWORD = Argument("password", "--password", "-w", help="Specifies the password of the compute target."
                                                         "This option can be skipped in the command to enter the "
                                                         "password using standard input.")

USERNAME = Argument("username", "--username", "-u", help="Specifies the compute target's username.")


SSH_KEY = Argument("ssh_key", "--use-azureml-ssh-key", "-k", help="Use ssh key to connect to remote target.",
                   action="store_true")

HIDE = Argument("hide", "--hide-password", "", help="If this option is specified then the password is not printed on "
                                                    "the terminal when a user types it. By default, the password "
                                                    "is printed on the terminal.",
                action="store_true", default=False)

PRIVATE_KEY_FILE = Argument("private_key_file", "--private-key-file", "",
                            help="Use this private key for initial connection to remote host (to install the Azure "
                                 "ML Workbench key).")

PRIVATE_KEY_PASSPHRASE = Argument("private_key_passphrase", "--private-key-passphrase", "",
                                  help="Passphrase for private key specified with the --private-key-file option.")


IMAGE_REPOSITORY_ADDRESS = Argument("image_repository_address", "--image-repository-address", "",
                                    help="Specifies the image repository address.")

IMAGE_REPOSITORY_USERNAME = Argument("image_repository_username", "--image-repository-username", "",
                                     help="Specifies the image repository username.")

IMAGE_REPOSITORY_PASSWORD = Argument("image_repository_password", "--image-repository-password", "",
                                     help="Specifies the image repository password. This option can be skipped in "
                                          "the command to enter the password using standard input.")

BASE_DOCKER_IMAGE = Argument("base_docker_image", "--base-docker-image", "",
                             help="Specifies the docker image to be used at the compute target.")

SUBSCRIPTION_ID = Argument("subscription_id", "--subscription-id", "", help="Specifies the subscription Id for "
                                                                            "the compute target.")


STORAGE_ACCOUNT_NAME = Argument("storage_account_name", "--storage-account-name", "",
                                help="Specifies the storage account name for the compute target.")


STORAGE_ACCOUNT_KEY = Argument("storage_account_key", "--storage-account-key", "",
                               help="Specifies the storage account key. This option can be skipped in the command to "
                                    "enter the key using standard input.")

FILE_SHARE_NAME = Argument("file_share_name", "--file-share-name", "", help="Specifies the azure file share name.")

COMPUTE_RESOURCE_ID = Argument("compute_resource_id", "--compute-resource-id", "-i",
                               help="Resource ID of the compute object to attach to the workspace.")
