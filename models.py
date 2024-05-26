from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SSHConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(128), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    pub_key = db.Column(db.Text, nullable=True)

    def __init__(self, host, port, username, password=None, pub_key=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.pub_key = pub_key

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    command = db.Column(db.String(128), nullable=False)
    ssh_connection_id = db.Column(db.Integer, db.ForeignKey('ssh_connection.id'), nullable=False)
    ssh_connection = db.relationship('SSHConnection', backref=db.backref('test_cases', lazy=True))
