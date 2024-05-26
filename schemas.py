from marshmallow import Schema, fields, validates, ValidationError, post_load
from models import SSHConnection, TestCase

class SSHConnectionSchema(Schema):
    id = fields.Int(dump_only=True)
    host = fields.Str(required=True)
    port = fields.Int(required=True)
    username = fields.Str(required=True)
    password = fields.Str(allow_none=True)
    pub_key = fields.Str(allow_none=True)

    @validates('password')
    def validate_password(self, value, **kwargs):
        if not value and not self.context.get('pub_key'):
            raise ValidationError('Either password or pub_key must be provided.')

    @validates('pub_key')
    def validate_pub_key(self, value, **kwargs):
        if not value and not self.context.get('password'):
            raise ValidationError('Either pub_key or password must be provided.')

    @post_load
    def make_ssh_connection(self, data, **kwargs):
        return SSHConnection(**data)

class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    command = fields.Str(required=True)
    ssh_connection_id = fields.Int(required=True)

    @post_load
    def make_test_case(self, data, **kwargs):
        return TestCase(**data)
