import os
import sys

print("Current working directory:", os.getcwd())
print("Directory listing of /app:", os.listdir("/app"))
print("Directory listing of /app/tests:", os.listdir(os.path.dirname(__file__)))
import pytest
from main import app as flask_app  # noqa: E402

# Add /app to sys.path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("flask_app type:", type(flask_app))
print("flask_app repr:", repr(flask_app))


@pytest.fixture
def client():
    return flask_app.test_client()
