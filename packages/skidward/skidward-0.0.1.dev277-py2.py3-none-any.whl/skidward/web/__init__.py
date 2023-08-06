from flask_admin import Admin

from skidward.app import app
from skidward.models import db, User, Role, Worker, Task, Job
from skidward.web.views import (
    UserAdmin,
    RoleAdmin,
    JobView,
    TaskView,
    WorkerView,
    RunView,
    TaskConfigure,
    SkidwardView,
    LogoutMenuLink,
    LoginMenuLink,
)


# Initializing admin with flask app, name and template type
admin = Admin(app, name="Skidward-Admin", template_mode="bootstrap3")

# Adding Models as Views to admin
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))
admin.add_view(WorkerView(Worker, db.session))
admin.add_view(TaskView(Task, db.session))
admin.add_view(JobView(Job, db.session))
admin.add_view(RunView(name="Run", endpoint="run_task", url="/admin/task"))
admin.add_view(
    TaskConfigure(name="Configure", endpoint="add_context", url="/admin/task")
)
admin.add_view(SkidwardView(name="Skidward-Home", endpoint="index", url="/"))
admin.add_link(LoginMenuLink(name="Login", endpoint="login", url="/login"))
admin.add_link(LogoutMenuLink(name="Logout", endpoint="logout", url="/logout"))


if __name__ == "__main__":
    app.run()
