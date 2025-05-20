from src.app import ma
from marshmallow import fields

class RoleSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    class Meta:
        fields = ("id", "name")