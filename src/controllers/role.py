from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import Role, db
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED
    