import pytest

from backend.main import app as flask_app
from backend.main import tax_data


@pytest.fixture(autouse=True)
def clear_tax_data():
    # run before each test
    tax_data.clear()
    yield
    # and after
    tax_data.clear()


@pytest.fixture
def app():
    # Configure Flask for testing
    flask_app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
