import os
import sys

import pytest

# Add /app to sys.path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app  # ✅ this should now work


@pytest.fixture
def client():
    return flask_app.test_client()
