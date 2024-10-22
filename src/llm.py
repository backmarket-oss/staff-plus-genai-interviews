import logging
import os

from google.auth import default
from google.auth.transport.requests import Request
from openai import OpenAI


def configure(
    project: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
    location: str = os.getenv("DEFAULT_GCP_REGION", "europe-west2"),
) -> OpenAI:
    """
    Configure the OpenAI client with GCP credentials by default.

    :param project: The GCP project name.
    :param location: The GCP location name.
    :return: The OpenAI client.
    """
    logging.info(f"Configure the OpenAI client with project: {project} and location: {location}")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set, must be set to use GCP credentials.")
    creds, _ = default()
    creds.refresh(Request())
    return OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{location}/endpoints/openapi",
        api_key=creds.token,
    )
