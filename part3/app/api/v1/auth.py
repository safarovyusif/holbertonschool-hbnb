from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services import facade

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()

    if not credentials or 'email' not in credentials or 'password' not in credentials:
        return jsonify({'error': 'Missing email or password'}), 400

    email = credentials['email']
    password = credentials['password']

    # 1. İstifadəçini tapırıq
    user = facade.get_user_by_email(email)

    # 2. Parolu yoxlayırıq
    if not user or not user.verify_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # 3. Token yaradırıq (istifadəçi ID-si və admin olub-olmadığı tokenin içində gizlənir)
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"is_admin": user.is_admin}
    )

    return jsonify({'access_token': access_token}), 200
