# MIT License
#
# Copyright (c) 2025 Victor Calderon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import

import argparse
import base64
import contextlib
import json
import logging
import os
import traceback
from argparse import ArgumentParser, HelpFormatter
from operator import attrgetter
from pathlib import Path
from typing import Dict, Optional

import boto3
import docker
import numpy as np
import pydash

__author__ = ["{{ cookiecutter.author_name }}"]
__maintainer__ = ["{{ cookiecutter.author_name }}"]
__all__ = [
    "check_environment_variables",
    "get_repository_metadata",
    "docker_build_and_push",
]

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)
logger.setLevel(logging.INFO)

# -------------------------------- SERVICES -----------------------------------


def _get_services(region_name: str) -> Dict:
    """
    Function to define the services used throughout the script.

    Parameters
    --------------
    region_name : str
        Name of the AWS region to use.

    Returns
    -------------
    services_dict : dict
        Dictionary containing the set of services to use.
    """
    # Main AWS session
    aws_session = boto3.session.Session(region_name=region_name)

    return {
        "ecr": aws_session.client("ecr"),
        "ssm": aws_session.client("ssm"),
        "docker": docker.from_env(),
    }


# -------------------------------- MISCELLANEOUS ------------------------------


def _show_params(params_dict: Dict):
    """
    Function to show the defined of the class.
    """
    msg = "-" * 50 + "\n"
    msg += "\t---- INPUT PARAMETERS ----" + "\n"
    msg += "" + "\n"
    # Keys to omit
    columns_to_omit = []
    # Sorting keys of dictionary
    keys_sorted = np.sort(list(params_dict.keys()))
    for key_ii in keys_sorted:
        if key_ii not in columns_to_omit:
            msg += f"\t>>> {key_ii} : {params_dict[key_ii]}\n"
    #
    msg += "\n" + "-" * 50 + "\n"
    logger.info(msg)

    return


def get_default_parameters() -> Dict:
    # sourcery skip: use-fstring-for-formatting
    """
    Function to determine the set of default parameters for the project.

    Returns
    ------------
    params_default_values_dict : dict
        Dictionary with the specified default variables.
    """
    # --- List of parameters
    params_arr = [
        "application_name",
        "region_name",
    ]
    # Extracting parameters from environment
    params_default_values_dict = {
        key: os.environ.get(key.upper()) for key in params_arr
    }
    # Definining initial dictionary
    params_default_values_dict["environment"] = os.environ["ENV"]

    return params_default_values_dict


# ----------------------------- INPUT PARAMETERS ------------------------------


def _str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        """
        Modifier for `argparse` help parameters, that sorts them alphabetically
        """
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def get_parser():
    """
    Function to get the input parameters to the script.
    """
    description = ""
    parser = ArgumentParser(
        description=description,
        formatter_class=SortingHelpFormatter,
    )

    # Option for whether or not to push the image to ECR repository.
    parser.add_argument(
        "--push",
        "-p",
        dest="push_to_repo",
        type=_str2bool,
        default=True,
        help="""
        Option for whether or not to push the image to ECR repository.
        [Default: '%(default)s']
        """,
    )
    #
    # Option for removing the local Docker image that was built.
    parser.add_argument(
        "--remove-image",
        "-rmi",
        dest="remove_image",
        type=_str2bool,
        default=True,
        help="""
        Option for removing the local Docker image that was built.
        [Default: '%(default)s']
        """,
    )
    # Name of the application
    parser.add_argument(
        "--application-name",
        "-app",
        dest="application_name",
        type=str,
        default="{{ cookiecutter.application_name }}",
        help="""
        Name of the application.
        [Default: '%(default)s']
        """,
    )
    # Environment name
    parser.add_argument(
        "--environment-name",
        "-env",
        dest="environment",
        type=str,
        default="prod",
        choices=["dev", "prod"],
        help="""
        Name of the environment to use.
        [Default: '%(default)s']
        """,
    )
    # AWS Region name
    parser.add_argument(
        "--region-name",
        "-r",
        dest="region_name",
        type=str,
        default="us-west-2",
        help="""
        Name of the AWS region to use.
        [Default: '%(default)s']
        """,
    )
    # Type of platform to use when building the Docker image
    parser.add_argument(
        "--platform",
        dest="platform",
        type=str,
        default="linux/amd64",
        help="""
        Type of platform to use when building the Docker image.
        [Default: '%(default)s']
        """,
    )

    return parser.parse_args()


# -------------------------------- FUNCTIONS ----------------------------------


def check_environment_variables():
    """
    Function to determine whether or not the set of environments variables
    are defined.

    Raises
    ----------
    ValueError : Error
        This error gets raised whenever the environment variable is not
        part of the environment.
    """
    # Defining set of environment variables
    variables_arr = []
    # Environment keys
    env_keys = [xx.lower() for xx in list(os.environ)]
    # Checking whether or not all variables are defined
    variables_defined_dict = {xx: xx in env_keys for xx in variables_arr}
    #
    # Set of undefined variables
    if sum(variables_defined_dict.values()) < len(variables_arr):
        for varname, exists_opt in variables_defined_dict.items():
            if not exists_opt:
                logger.warning(f">>> `{varname}` is not defined!!")

        raise ValueError("Missing variables!!")


def get_repository_metadata(params_dict: Dict) -> Dict:
    # sourcery skip: use-fstring-for-formatting
    """
    Function to extract the metadata of the Docker image and its ECR
    repository.

    Parameters
    -------------
    params_dict : dict
        Dictionary with set of input parameters

    Returns
    -----------
    ecr_metadata : dict
        Dictionary containing the metadata of the ECR repository.
    """
    # --- Reading in data from the Parameter Store
    # Defining the parameter key
    param_key = "/{}/{}/config".format(
        params_dict["application_name"],
        params_dict["environment"],
    )
    # --- Extracting repository's metadata
    logger.info(f">>> Environment: `{params_dict['environment']}` ")
    logger.info(f">>> Reading `{param_key}` SSM Parameter")
    #
    response = params_dict["services"]["ssm"].get_parameter(
        Name=param_key,
        WithDecryption=True,
    )
    # Extracting repository's metadata
    infra_config = json.loads(pydash.get(response, "Parameter.Value"))
    #
    infra_elements = [
        "ecr_repo",
        "ecr_registry_id",
        "ecr_repository_name",
    ]
    # Ouptutting values as dictionary
    ecr_metadata = {xx: infra_config[xx] for xx in infra_elements}
    #
    for elem, elem_value in ecr_metadata.items():
        logger.info(f">>       `{elem}` : `{elem_value}")

    return ecr_metadata


def _docker_login(params_dict: Dict):
    """
    Function for logging into Docker for AWS.

    Parameters
    -------------
    params_dict : dict
        Dictionary with set of input parameters
    """
    logger.info(">>> Logging into Docker ....")
    # Get token
    token = params_dict["services"]["ecr"].get_authorization_token()
    # Extract username and password
    username, password = (
        base64.b64decode(token["authorizationData"][0]["authorizationToken"])
        .decode()
        .split(":")
    )
    # Registry ID
    registry = token["authorizationData"][0]["proxyEndpoint"]
    # Login to Docker
    try:
        params_dict["services"]["docker"].login(
            username,
            password,
            registry=registry,
        )
    except Exception:
        msg = traceback.format_exc()
        logger.error(msg)
    #
    logger.info(">>> Logging into Docker .... DONE")


def docker_build_and_push(
    ecr_metadata: Dict,
    params_dict: Dict,
    push_image: Optional[bool] = True,
    remove_local_image: Optional[bool] = True,
):  # sourcery skip: use-fstring-for-formatting
    """
    Function to build the Docker image and deploy it to the Docker repository.

    Parameters
    --------------
    ecr_metadata : dict
        Dictionary containing the metadata of the ECR repository.

    params_dict : dict
        Dictionary with set of input parameters

    push_image : bool, optional
        If ``True``, the function will push the image to the ECR repository.
        Otherwise, it will just build the image. This variable is set
        to ``True`` by default.

    remove_local_image : bool, optional
        If ``True``, the function will remove the local image that was just
        built. This variable is set to ``True`` by default.
    """
    logger.info(">>> Building and pushing Docker image ....")
    # --- Building Docker image
    # Docker context
    docker_context = str(
        Path(__file__)
        .joinpath(
            "..",
            "..",
        )
        .resolve()
    )
    # Path to Dockerfile
    docker_filepath = str(
        Path(__file__)
        .joinpath(
            "..",
            "Dockerfile",
        )
        .resolve()
    )
    # Build arguments
    docker_build_args = {
        "PLATFORM": params_dict["platform"],
        "ENVIRONMENT": params_dict["environment"],
    }
    # Docker image name and tag
    image_name = ecr_metadata["ecr_repo"]
    image_tag = "latest"
    #
    logger.info(f">> docker_context:    `{docker_context}")
    logger.info(f">> docker_filepath:   `{docker_filepath}")
    logger.info(f">> image_name:        `{image_name}")
    logger.info(f">> image_tag:         `{image_tag}")
    # Check that Dockerfile exists
    if not Path(docker_filepath).exists():
        msg = f">> Dockerfile `{docker_filepath}` does not exist!"
        logger.error(msg)
        raise FileNotFoundError(msg)
    # -- Building image
    logger.info(f">> Building docker image: `{image_name}` ...")
    #
    params_dict["services"]["docker"].images.build(
        path=docker_context,
        tag=f"{image_name}:{image_tag}",
        nocache=True,
        rm=False,
        dockerfile=str(Path(docker_filepath).relative_to(docker_context)),
        platform=params_dict["platform"],
        buildargs=docker_build_args,
    )
    logger.info(f">> Building docker image: `{image_name}` ... DONE")
    # ---  Validate login
    _docker_login(params_dict=params_dict)
    # --- Pushing to ECR container
    if push_image:
        logger.info(f">> Pushing image to repository`{image_name}` ...")
        #
        params_dict["services"]["docker"].images.push(
            repository=image_name,
            tag=image_tag,
        )
        #
        logger.info(f">> Pushing image to repository`{image_name}` ... DONE")
    # Removing local image
    if remove_local_image:
        with contextlib.suppress(Exception):
            params_dict["services"]["docker"].images.remove(
                image_name,
                force=True,
            )
    #
    logger.info(">>> Building and pushing Docker image .... DONE")


def main(params_dict: Dict):
    # Extracting default parameters
    params_default_values_dict = get_default_parameters()
    # Showing input parameters
    for key, key_val in params_default_values_dict.items():
        if (key not in params_dict) and (key_val is not None):
            params_dict[key] = key_val
    # Showing input parameters
    _show_params(params_dict=params_dict)
    # Initializing services
    params_dict["services"] = _get_services(
        region_name=params_dict["region_name"],
    )
    # Checking environment variables
    check_environment_variables()
    # Extracting ECR repository's metadata
    ecr_metadata = get_repository_metadata(params_dict=params_dict)
    # Build and push docker image
    docker_build_and_push(
        ecr_metadata=ecr_metadata,
        params_dict=params_dict,
        push_image=params_dict["push_to_repo"],
        remove_local_image=params_dict["remove_image"],
    )

    return


if __name__ == "__main__":
    # Input parameters
    params_dict = vars(get_parser())
    #
    main(params_dict=params_dict)
