from flask import Blueprint, request, jsonify, abort
from app.services import facade

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def create_user():
    """Yeni istifadəçi yaradır (Parol ilə)"""
    user_data = request.get_json()
    
    if not user_data:
        return jsonify({"error": "Invalid input"}), 400

    if 'first_name' not in user_data or 'last_name' not in user_data or 'email' not in user_data or 'password' not in user_data:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = facade.get_user_by_email(user_data['email'])
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    new_user = facade.create_user(user_data)
    
    return jsonify({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email
    }), 201

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """İstifadəçini ID ilə gətirir (Parolsuz)"""
    user = facade.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }), 200

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    user = facade.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.update(user_data)
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }), 200
