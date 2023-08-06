import pytest

from skidward.backend import RedisBackend


@pytest.fixture(autouse=True)
def enable_testing(monkeypatch):
    monkeypatch.setenv("TESTING", "True")


@pytest.fixture()
def backend():
    dummy_backend = RedisBackend()
    yield dummy_backend
    dummy_backend.dummy_backend.erase()
