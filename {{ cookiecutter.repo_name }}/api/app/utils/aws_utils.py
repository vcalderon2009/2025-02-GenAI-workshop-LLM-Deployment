# MIT License
#
# Copyright 2025, Victor Calderon
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

from app.utils.logging import get_logger
import boto3
from botocore.exceptions import ClientError
import json

__author__ = ["Victor Calderon"]
__all__ = ["get_aws_secret"]

logger = get_logger(__name__)


def get_aws_secret(
    secret_name: str,
    region_name: str,
) -> str:
    """
    Function to extract the value of a 'Secret' in AWS.
    """
    # Creating an AWS client
    session = boto3.session.Session()
    secrets_client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        get_secret_value_response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logger.error(
            f">>> Error while reading in secret '{secret_name}'. e: {e}"
        )
        raise e

    secret = json.loads(get_secret_value_response["SecretString"])

    return secret
