from unittest import mock

from flask_login import current_user

from skidward.models import User, Worker, Task


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


def test_configure_asks_for_context_and_save_in_db_correctly(
    test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    response = test_client.get("/admin/task/configure/1", follow_redirects=True)
    assert b"Add Configuration" in response.data
    test_client.post(
        "/admin/task/configure/1",
        data=dict(key="new_key", value="new_value"),
        follow_redirects=True,
    )
    task = Task.query.get(1)
    assert task.context == {"new_key": "new_value"}
    assert type(task.context) == dict


def test_configured_run_takes_new_context_but_does_not_save_in_db(
    backend, test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    response = test_client.post(
        "/admin/task/configure/1?temp_run=True",
        data=dict(key="tmp_key", value="tmp_value"),
        follow_redirects=True,
    )
    assert b"RUNNING TASK" in response.data
    # assert b"Context: {'tmp_key': 'tmp_value'}" in response.data
    # Going to Fetch request args here and verify given context
    task = Task.query.get(1)
    assert task.context == {"test_key": "test_value"}


@mock.patch("skidward.backend.RedisDummyBackend")
def test_quick_run_pushes_task_id_to_redis_and_redirects_to_run_task(
    mock_redis, test_client, backend, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    mock_redis.return_value = backend
    response = test_client.get("/admin/task/run/1", follow_redirects=True)
    redis_tasks = backend.lrange("MANUAL_RUN", 0, -1)

    assert b"1" in redis_tasks
    assert b"RUNNING TASK" in response.data


@mock.patch("skidward.backend.RedisDummyBackend")
def test_configured_run_pushes_dict_of_task_with_context_to_redis(
    mock_redis, test_client, backend, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    mock_redis.return_value = backend
    test_client.post(
        "admin/task/configure/1?temp_run=True",
        data=dict(key="tmp_key", value="tmp_value"),
        follow_redirects=True,
    )
    redis_tasks = backend.lrange("MANUAL_RUN", 0, -1)
    for t in redis_tasks:
        assert t["task"] == "1"
        assert t["context"] == "{'tmp_key': 'tmp_value'}"


def test_manual_run_redirects_to_configure_if_no_context_is_present(
    test_client, init_database
):
    test_client.post(
        "/login",
        data=dict(email="test@test.com", password="123"),
        follow_redirects=True,
    )
    worker = Worker.query.first()
    new_task = Task(name="New_Task", worker=worker)
    init_database.session.add(new_task)
    init_database.session.commit()
    task = Task.query.filter_by(name="New_Task").first()
    assert task is not None
    assert task.id == 2
    assert not task.context
    response = test_client.get("/admin/task/run/2", follow_redirects=True)
    assert b"Add Configuration" in response.data
