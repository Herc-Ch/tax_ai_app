import main as bm
import pytest
from main import app as flask_app
from main import tax_data


@pytest.fixture(autouse=True)
def clear_tax_data():
    # run before each test
    tax_data.clear()
    yield
    # and after
    tax_data.clear()


# configures the flask app in testing mode
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


# returns a flask test client that simulates HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()


class DummyResp:
    def __init__(self, text):
        self.choices = [type("C", (), {"message": type("M", (), {"content": text})})]


@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    monkeypatch.setattr(
        bm.client.chat.completions,
        "create",
        lambda **kw: DummyResp("This is fake advice"),
    )
    yield
