from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

places_bp = Blueprint('places', __name__)

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new place."""
    current_user_id = get_jwt_identity()
    place_data = request.get_json()
    
    # Check if necessary fields exist
    if 'title' not in place_data or 'price' not in place_data:
        return jsonify({'error': 'Missing title or price'}), 400

    new_place = facade.create_place(place_data)
    # Update owner_id to match the logged-in user
    new_place.owner_id = current_user_id
    
    return jsonify({
        'id': new_place.id,
        'title': new_place.title,
        'price': new_place.price,
        'owner_id': new_place.owner_id
    }), 201

@places_bp.route('/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update a place. Admins can bypass ownership check."""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # Authorization: Allow if user is owner OR is admin
    if place.owner_id != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized action'}), 403

    data = request.get_json()
    place.update(data)

    return jsonify({'message': 'Place updated successfully'}), 200

@places_bp.route('/', methods=['GET'])
def get_places():
    """Retrieve all places."""
    places = facade.get_all_places()
    return jsonify([
        {'id': p.id, 'title': p.title, 'price': p.price} for p in places
    ]), 200

@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific place."""
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    return jsonify({
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner_id': place.owner_id
    }), 200
