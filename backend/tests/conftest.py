import os
import sys

import pytest

# Add /app to sys.path so we can import app.py
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app  # noqa: E402
# print("flask_app type:", type(flask_app))


@pytest.fixture
def client():
    return flask_app.test_client()
