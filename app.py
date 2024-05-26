import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from models import db, SSHConnection, TestCase
from schemas import SSHConnectionSchema, TestCaseSchema

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

ssh_connection_schema = SSHConnectionSchema()
ssh_connections_schema = SSHConnectionSchema(many=True)
test_case_schema = TestCaseSchema()
test_cases_schema = TestCaseSchema(many=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

# Web routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh-connections')
def ssh_connections():
    return render_template('ssh_connections.html')

@app.route('/test-cases')
def test_cases():
    return render_template('test_cases.html')

# SSH Connection API endpoints
@app.route('/api/ssh_connections', methods=['POST'])
def add_ssh_connection():
    host = request.form['host']
    port = request.form['port']
    username = request.form['username']
    password = request.form.get('password')
    pub_key = None

    if 'pub_key' in request.files:
        file = request.files['pub_key']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pub_key = filename

    new_connection = SSHConnection(
        host=host,
        port=port,
        username=username,
        password=password,
        pub_key=pub_key
    )

    try:
        db.session.add(new_connection)
        db.session.commit()
        return jsonify(ssh_connection_schema.dump(new_connection)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/api/ssh_connections', methods=['GET'])
def get_ssh_connections():
    connections = SSHConnection.query.all()
    return jsonify(ssh_connections_schema.dump(connections)), 200

@app.route('/api/ssh_connections/<int:id>', methods=['DELETE'])
def delete_ssh_connection(id):
    connection = SSHConnection.query.get_or_404(id)
    db.session.delete(connection)
    db.session.commit()
    return '', 204

# Test Case API endpoints
@app.route('/api/test_cases', methods=['POST'])
def add_test_case():
    data = request.json
    new_test_case = test_case_schema.load(data)
    db.session.add(new_test_case)
    db.session.commit()
    return jsonify(test_case_schema.dump(new_test_case)), 201

@app.route('/api/test_cases', methods=['GET'])
def get_test_cases():
    test_cases = TestCase.query.all()
    return jsonify(test_cases_schema.dump(test_cases)), 200

@app.route('/api/test_cases/<int:id>', methods=['DELETE'])
def delete_test_case(id):
    test_case = TestCase.query.get_or_404(id)
    db.session.delete(test_case)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
