from src.app import ma
from marshmallow import fields
from src.views.role import RoleSchema
from src.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        
    # id = ma.auto_field()
    # username = ma.auto_field()
    # role = ma.Nested(RoleSchema)
    
class UserIdParameter(ma.Schema):
    user_id=fields.Int(required=True, strict=True)
    
    
class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)
   
   
   
   
   
       
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# from src.models.user import User  # ajuste o caminho conforme seu projeto

# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True
#         include_fk = True

#     id = auto_field()
#     username = auto_field()
#     role_id = auto_field()