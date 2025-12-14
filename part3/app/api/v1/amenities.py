from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/', methods=['POST'])
@jwt_required()
def create_amenity():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin privileges required'}), 403

    data = request.get_json()
    new_amenity = facade.create_amenity(data)
    return jsonify({'id': new_amenity.id, 'name': new_amenity.name}), 201

@amenities_bp.route('/<amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin privileges required'}), 403

    data = request.get_json()
    amenity = facade.update_amenity(amenity_id, data)
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
        
    return jsonify({'message': 'Amenity updated successfully'}), 200

@amenities_bp.route('/', methods=['GET'])
def get_amenities():
    amenities = facade.get_all_amenities()
    return jsonify([{'id': a.id, 'name': a.name} for a in amenities]), 200

@amenities_bp.route('/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = facade.get_amenity(amenity_id)
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify({'id': amenity.id, 'name': amenity.name}), 200
