# auth.py

from flask import Blueprint, jsonify, request
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    code = data.get('signCode')
    if code != os.getenv('SIGN_CODE'):
        return jsonify(message="Invalid sign code"), 401

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify(message="User already exists"), 409

    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)

    new_user = User(email=data['email'], password=hashed_password.decode('utf-8'), name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=user.id, additional_claims={"name": user.name})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Bad Email or Password"), 401
