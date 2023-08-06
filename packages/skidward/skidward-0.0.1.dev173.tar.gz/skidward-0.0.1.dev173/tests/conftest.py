from typing import Dict
from unittest import mock

import pkg_resources as pkg
import pytest

# import before skidward.models to avoid circular imports
from skidward import web
from skidward import JobStatus
from skidward.backend import RedisBackend
from skidward.models import db, Job, Task, Worker
from worker_detector.namespace_module_manager import NamespaceModuleManager


@pytest.fixture(autouse=True)
def enable_testing(monkeypatch):
    monkeypatch.setenv("TESTING", "True")
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")


@pytest.fixture()
def init_database():
    db.create_all()
    worker_one = Worker(name="real_name")
    db.session.add(worker_one)
    db.session.commit()

    task_one = Task(
        name="task_1",
        worker=worker_one,
        context={"setting_1": "value_1"},
        cron_string="*/2 * * * *",
    )
    db.session.add(task_one)
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def real_namespace() -> str:
    return "skidward.real.name.space"


class MockEntryPoint(pkg.EntryPoint):
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name
        self.attrs = []
        self.extras = []
        self.dist = []

    def load(self, *args, **kwargs) -> pkg.EntryPoint:
        return MockEntryPoint(self.name, self.module_name)

    def start(self, context):
        return True


class MockNamespaceModuleManager(NamespaceModuleManager):
    def _get_module_entry_points_on_namespace(self) -> Dict[str, pkg.EntryPoint]:
        if self.namespace == "skidward.real.name.space":
            return {
                "real_name": MockEntryPoint("real-name", "real_name"),
                "other_name": MockEntryPoint("other-name", "other_name"),
            }

        return super()._get_module_entry_points_on_namespace()


@pytest.fixture
def mock_namespace_module_manager() -> MockNamespaceModuleManager:
    return MockNamespaceModuleManager("skidward.real.name.space")


@pytest.fixture()
def backend():
    dummy_backend = RedisBackend()
    yield dummy_backend
    dummy_backend.dummy_backend.erase()
