from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    review_data = request.get_json()

    if 'place_id' not in review_data:
        return jsonify({'error': 'Place ID is required'}), 400

    place = facade.get_place(review_data['place_id'])
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # 1. Qayda: Öz evinə rəy yaza bilməzsən
    if place.owner_id == current_user_id:
        return jsonify({'error': 'You cannot review your own place'}), 400

    # 2. Qayda: Eyni evə ikinci dəfə rəy yaza bilməzsən
    existing_reviews = facade.get_reviews_by_place(place.id)
    for r in existing_reviews:
        if r.user_id == current_user_id:
            return jsonify({'error': 'You have already reviewed this place'}), 400

    review_data['user_id'] = current_user_id
    new_review = facade.create_review(review_data)

    return jsonify({
        "id": new_review.id,
        "text": new_review.text,
        "rating": new_review.rating
    }), 201

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    # 3. Qayda: Yalnız öz rəyini dəyişə bilərsən
    if review.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    facade.update_review(review_id, data)
    return jsonify({"message": "Review updated successfully"}), 200

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user_id = get_jwt_identity()
    
    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    # 4. Qayda: Yalnız öz rəyini silə bilərsən
    if review.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    facade.delete_review(review_id)
    return jsonify({"message": "Review deleted successfully"}), 200
