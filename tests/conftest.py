import pytest

from main import create_app
from repository.book_repository import clear


@pytest.fixture(scope="function")
def app():
    return create_app({"TESTING": True})


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def clear_books():
    clear(None)
    yield
    clear(None)


@pytest.fixture(scope="function")
def db():
    clear(None)
    yield None
    clear(None)