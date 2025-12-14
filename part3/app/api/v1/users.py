from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
@jwt_required(optional=True)
def create_user():
    claims = get_jwt()
    is_admin_request = False
    
    # Əgər token varsa və is_admin=True isə
    if claims and claims.get('is_admin'):
        is_admin_request = True

    user_data = request.get_json()
    
    # Email yoxlanışı
    existing_user = facade.get_user_by_email(user_data.get('email'))
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    # Admin deyilsə, is_admin sahəsini zorla False edirik
    if not is_admin_request:
        user_data['is_admin'] = False

    new_user = facade.create_user(user_data)
    return jsonify({'id': new_user.id, 'email': new_user.email, 'is_admin': new_user.is_admin}), 201

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
    claims = get_jwt()
    current_user_id = get_jwt_identity()
    is_admin = claims.get('is_admin', False)

    # İcazə: Ya Admin olmalıdır, ya da istifadəçi özü
    if not is_admin and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    user_data = request.get_json()
    user = facade.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Email/Parol dəyişimi: Adi istifadəçiyə qadağandır
    if (not is_admin) and ('email' in user_data or 'password' in user_data):
        return jsonify({'error': 'You cannot modify email or password'}), 400
    
    # Admin email dəyişirsə, unikal olduğunu yoxlamalıyıq
    if is_admin and 'email' in user_data:
        existing = facade.get_user_by_email(user_data['email'])
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email already in use'}), 400

    user.update(user_data)
    return jsonify({'message': 'User updated successfully'}), 200
