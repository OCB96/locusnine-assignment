# coding=utf-8

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ENUM

from .entity import Entity, Base

from marshmallow import Schema, fields, validate
from pprint import pprint


class User(Entity, Base):
    __tablename__ = 'users'

    name = Column(String)
    email = Column(String)
    role_type = Column(String, ENUM('Admin', 'Customer Executive', name='role_type'))
    mobile_number = Column(String, nullable=True)
    activity_status = Column(String)

    def __init__(self, name, email, role_type, mobile_number, activity_status, created_by):
        Entity.__init__(self, created_by)
        self.name = name
        self.email = email
        self.role_type = role_type
        self.mobile_number = mobile_number
        self.activity_status = activity_status

class UserSchema(Schema):
    id = fields.Number()
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    role_type = fields.Str(validate=validate.OneOf(["Admin", "Customer Executive"]), required=True)
    mobile_number = fields.Str()
    activity_status = fields.Str(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()


