from flask import Flask

from .extensions import appbuilder, db
from .examples.api import ExampleApi

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        db.init_app(app)
        #db.create_all()
        appbuilder.init_app(app, db.session)
        # Registering the views and APIs
        appbuilder.add_api(ExampleApi)
    return app
