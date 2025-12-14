from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

places_bp = Blueprint('places', __name__)

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    """Yalnız qeydiyyatlı istifadəçilər ev yarada bilər"""
    current_user_id = get_jwt_identity()
    place_data = request.get_json()

    # Sahibin ID-sini avtomatik token-dən götürürük
    place_data['owner_id'] = current_user_id
    
    new_place = facade.create_place(place_data)
    return jsonify({
        "id": new_place.id,
        "title": new_place.title,
        "price": new_place.price,
        "owner_id": new_place.owner_id
    }), 201

@places_bp.route('/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Yalnız evin sahibi evi yeniləyə bilər"""
    current_user_id = get_jwt_identity()
    place_data = request.get_json()
    
    place = facade.get_place(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404

    # SAHİBLİK YOXLAMASI:
    if place.owner_id != current_user_id:
        return jsonify({"error": "Unauthorized action"}), 403

    facade.update_place(place_id, place_data)
    return jsonify({"message": "Place updated successfully"}), 200

@places_bp.route('/', methods=['GET'])
def get_places():
    """Hər kəs evlərə baxa bilər (Public)"""
    places = facade.get_all_places()
    return jsonify([
        {"id": p.id, "title": p.title, "price": p.price} for p in places
    ]), 200

@places_bp.route('/<place_id>', methods=['GET'])
def get_place_detail(place_id):
    """Hər kəs evin təfərrüatına baxa bilər (Public)"""
    place = facade.get_place(place_id)
    if not place:
        return jsonify({"error": "Place not found"}), 404
    
    return jsonify({
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "owner_id": place.owner_id
    }), 200
