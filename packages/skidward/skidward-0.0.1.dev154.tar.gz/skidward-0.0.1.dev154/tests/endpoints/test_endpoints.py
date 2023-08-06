from flask_login import current_user

from skidward.models import User, Worker


def test_it_loads_the_app(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200


def test_it_requires_login_to_access_home_page(test_client):
    response = test_client.get("/", follow_redirects=True)
    assert b"Please log in to access this page" in response.data


def test_it_logs_in_correct_user(test_client, init_database):
    with test_client:
        response = test_client.post(
            "/login",
            data=dict(email="test@test.com", password="123"),
            follow_redirects=True,
        )
        assert current_user.email == "test@test.com"


def test_it_creates_new_user_in_the_database(test_client, init_database):
    user = User.query.filter_by(email="test@test.com").first()
    assert user is not None
    assert user.email == "test@test.com"
    assert user.username == "testuser"


def test_it_redirects_to_home_on_login(test_client, init_database):
    response = test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    assert b"Scheduler For Python Scripts" in response.data


def test_it_logs_out_correctly_and_redirects_to_login(test_client, init_database):
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in" in response.data


def test_it_creates_worker_and_displays_in_list(test_client, init_database):
    response = test_client.post(
        "/admin/worker/new/", data=dict(name="test_worker"), follow_redirects=True
    )
    assert b"Skidward-Admin" in response.data
    assert b"list" in response.data
    worker = Worker.query.filter_by(name="test_worker").first()
    assert worker is not None
    assert worker.name == "test_worker"
