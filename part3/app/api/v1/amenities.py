from flask import Blueprint, jsonify

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/')
def get_amenities():
    return jsonify({"message": "Amenities list placeholder"}), 200
