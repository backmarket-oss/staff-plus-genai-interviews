from src.llm import configure

import pytest


def test_configure_no_gcp_project():
    match = "GOOGLE_CLOUD_PROJECT environment variable is not set, must be set to use GCP credentials."
    with pytest.raises(ValueError, match=match):
        configure(project="")
