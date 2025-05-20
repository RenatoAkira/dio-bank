from http import HTTPStatus

from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy import inspect
from src.models import User, db
from src.views.user import UserSchema, CreateUserSchema
from src.utils import requires_role
from flask_jwt_extended import jwt_required
from src.app import bcrypt

app = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
        )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created!"}, HTTPStatus.CREATED

@jwt_required()
@requires_role("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)
    #return [
    #    {
    #        "id": user.id,
    #        "username": user.username,
    #        "role": {
    #            "id": user.role_id,
    #            "name": user.role.name,
    #        },
    #    }  
    #    for user in users
    #]

@app.route("/", methods=["GET", "POST"])
def list_or_create_user():    
    if request.method == "POST":
        return _create_user()
    else:
        return {"users": _list_users()}

@app.route("/<int:user_id>")
def get_user(user_id):
    """User detail view.
    ---
    get:
      tags:
        - user
      parameters:
        - in: path
          name: user_id
          schema: UserIdParameter
      responses:
        200:
          description: Successful operation
          content:
            application/json:
              schema: UserSchema
    """
    
    user = db.get_or_404(User, user_id)
    return{
        "id": user.id,
        "username": user.username,
    }

@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    
    return{
        "id": user.id,
        "username": user.username,
    }

@app.route("/<int:user_id>", methods= ["DELETE"])
def delete_user(user_id):
    """User delete view.
    ---
    delete:
      tags:
        - user
      summary: Deletes a user
      description: delete a user
      parameters:
        - in: path
          name: user_id
          schema: UserIdParameter
      responses:
        204:
          description: Successful operation
        404:
          description: Not found user
    """
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
