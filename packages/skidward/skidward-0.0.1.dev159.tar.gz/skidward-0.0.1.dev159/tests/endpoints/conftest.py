import pytest
import os

from skidward.web import app
from skidward.models import db, User, Worker


def create_app():
    app.config["TESTING"] = os.getenv("TESTING")
    app.config["WTF_CSRF_ENABLED"] = os.getenv("WTF_CSRF_ENABLED")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    return app


@pytest.fixture()
def test_client():
    flask_app = create_app()
    client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def init_database():
    db.create_all()
    user1 = User(email="test@test.com", username="testuser", password="123")
    db.session.add(user1)
    worker1 = Worker(name="Test_Worker")
    db.session.add(worker1)
    db.session.commit()
    yield db
    db.drop_all()


@pytest.fixture(autouse=True)
def enable_debugging(monkeypatch):
    monkeypatch.setenv("TESTING", "True")
