from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    """Create a new review."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'place_id' not in data or 'text' not in data or 'rating' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    place = facade.get_place(data['place_id'])
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # Rule: Use cannot review their own place
    if place.owner_id == current_user_id:
        return jsonify({'error': 'You cannot review your own place'}), 400
    
    # Rule: User cannot review the same place twice
    all_reviews = facade.get_all_reviews()
    for r in all_reviews:
        if r.place_id == data['place_id'] and r.user_id == current_user_id:
            return jsonify({'error': 'You have already reviewed this place'}), 400

    new_review = facade.create_review(data)
    new_review.user_id = current_user_id
    
    return jsonify({
        'id': new_review.id,
        'place_id': new_review.place_id,
        'user_id': new_review.user_id,
        'text': new_review.text,
        'rating': new_review.rating
    }), 201

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review. Admins can bypass ownership check."""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    # Authorization: Allow if user is author OR is admin
    if review.user_id != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized action'}), 403

    data = request.get_json()
    review.update(data)
    return jsonify({'message': 'Review updated successfully'}), 200

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review. Admins can bypass ownership check."""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    # Authorization: Allow if user is author OR is admin
    if review.user_id != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized action'}), 403

    facade.delete_review(review_id)
    return jsonify({'message': 'Review deleted successfully'}), 200

@reviews_bp.route('/places/<place_id>', methods=['GET'])
def get_reviews_by_place(place_id):
    """Get all reviews for a specific place."""
    all_reviews = facade.get_all_reviews()
    place_reviews = [r for r in all_reviews if r.place_id == place_id]
    
    return jsonify([
        {'id': r.id, 'text': r.text, 'rating': r.rating} for r in place_reviews
    ]), 200
