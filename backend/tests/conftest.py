import os

print("Current working directory:", os.getcwd())
print("Directory listing of /app:", os.listdir("/app"))
print("Directory listing of /app/tests:", os.listdir(os.path.dirname(__file__)))
import pytest
from main import app as flask_app  # noqa: E402

print("flask_app type:", type(flask_app))
print("flask_app repr:", repr(flask_app))


@pytest.fixture
def client():
    return flask_app.test_client()
