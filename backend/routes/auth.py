from backend import app, db
from backend.routes import build_error
from backend.models import User
from flask import request, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, current_user

# if logged in, return the user's email address
@app.route('/auth/me', methods=["GET"])
@login_required
def check_auth():
    return jsonify({"email": current_user.email}), 200

@app.route('/auth/register', methods=["POST"])
def register_account():
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'email' not in body or 'password' not in body:
        return build_error("Email and pasword both required", 400)
    
    email = body['email']
    password = body['password']
    
    if len(password) < 8:
        return build_error("Password must be at least 8 characters", 400)
    
    if User.query.filter_by(email=email).first():
        return build_error("User with email address already exists", 400)
    
    new_user = User(email=email, hashed_password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=True)
    
    # return 201 Created upon sucessful response
    return "", 201

@app.route('/auth/login', methods=['POST'])
def login_account():
    body = request.get_json()
    if body == None:
        return build_error("No JSON body provided", 400)
    if 'email' not in body or 'password' not in body:
        return build_error("Email and pasword both required", 400)
    
    email = body['email']
    password = body['password']
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.hashed_password, password):
        return build_error("Invalid username or password", 401)
    
    login_user(user, remember=True)
    
    return '', 200

@app.route('/auth/logout', methods=['POST'])
@login_required
def logout_account():
    logout_user()
    return "", 200