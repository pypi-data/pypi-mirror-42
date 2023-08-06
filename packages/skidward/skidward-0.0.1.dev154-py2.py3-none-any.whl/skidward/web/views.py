from flask_admin.menu import MenuLink
from wtforms.fields import PasswordField
from flask_admin.form import fields
from flask_admin.model.template import EndpointLinkRowAction
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_security import login_required, current_user, utils

from skidward.models import Task
from skidward.backend import RedisBackend


class UserAdmin(ModelView):
    form_excluded_columns = ("password",)

    def is_accessible(self):
        return current_user.has_role("admin")

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField("New Password")
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = utils.hash_password(model.password2)


class RoleAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role("admin")


class TaskView(ModelView):

    column_extra_row_actions = [
        EndpointLinkRowAction(
            icon_class="glyphicon glyphicon-play",
            endpoint="run_task.run_task",
            title="Run_Task",
            id_arg="task_id",
        )
    ]

    form_overrides = {"context": fields.JSONField}


class JobView(ModelView):

    column_list = ["task", "ran_at", "state"]
    column_labels = dict(task="Jobs", state="Status")


class SkidwardView(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        return self.render("index.html")


class RunView(AdminIndexView):
    @expose("/run/<task_id>")
    @login_required
    def run_task(self, task_id):
        task = Task.query.get(task_id)
        redis_client = RedisBackend()
        redis_client.lpush("MANUAL_RUN", task_id)
        return self.render("task/run_task.html", name=task.name, context=task.context)


class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
