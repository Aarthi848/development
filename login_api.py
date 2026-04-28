from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# In-memory user store (replace with DB in production)
users = {}


@app.route('/api/login', methods=['POST'])
def login():
    """Login API endpoint for TEST-3"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    user = users.get(username)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate JWT token
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    users[username] = {'password': hashed_password}

    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
