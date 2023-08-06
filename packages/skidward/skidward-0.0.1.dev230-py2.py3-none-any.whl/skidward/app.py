import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security

from skidward.models import db, User, Role


app = Flask(__name__, template_folder="web/templates")

app.debug = os.getenv("FLASK_DEBUG")
# Setting any FLASK_ADMIN_SWATCH(Theme Template)
app.config["FLASK_ADMIN_SWATCH"] = os.getenv("FLASK_ADMIN_SWATCH")

# Setting up Postgres Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Setting up a secret key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SECURITY_PASSWORD_SALT")
app.config["SECURITY_PASSWORD_HASH"] = os.getenv("SECURITY_PASSWORD_HASH")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)


db.init_app(app)
security = Security(app, SQLAlchemyUserDatastore(db, User, Role))

with app.app_context():
    db.create_all()
