from flask import Flask

from projects.api import projects_pb
from users.api import users_bp

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
conf_file = os.environ.get("MYAPP_CONF_FILE", os.path.join(basedir, "config.py"))
app.config.from_pyfile(conf_file)

db = SQLAlchemy(app)

app.register_blueprint(projects_pb)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(port=5000)

