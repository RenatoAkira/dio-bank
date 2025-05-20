import os
import click

from flask import Flask, current_app
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from flask_bcrypt import Bcrypt   
from flask import json
from werkzeug.exceptions import HTTPException
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
spec = APISpec(
    title="DIO Bank",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="DIO Bank API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


def create_app(environment=os.environ["ENVIRONMENT"]):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #register cli commands
    app.cli.add_command(init_db_command)
    
    # Initialiaze extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    
    # register blueprints
    from src.controllers import user, auth, role
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    
    @app.route("/docs")
    def docs():
        return spec.path(view=user.get_user).to_dict()

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    
    return app