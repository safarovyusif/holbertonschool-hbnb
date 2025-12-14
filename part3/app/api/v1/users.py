from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    existing_user = facade.get_user_by_email(user_data.get('email'))
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    new_user = facade.create_user(user_data)
    return jsonify({'id': new_user.id, 'email': new_user.email}), 201

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = facade.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}), 200

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    
    # 1. Başqasının profilini dəyişə bilməzsən
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
        
    user_data = request.get_json()
    
    # 2. Email və Parolu dəyişmək qadağandır
    if 'email' in user_data or 'password' in user_data:
         return jsonify({'error': 'You cannot modify email or password'}), 400

    user = facade.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.update(user_data)
    return jsonify({'message': 'User updated successfully'}), 200
