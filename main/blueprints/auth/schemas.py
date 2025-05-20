from marshmallow import Schema, fields

class LoginSchema(Schema):
    matricula = fields.Int(required=True)
    senha = fields.Str(required=True)