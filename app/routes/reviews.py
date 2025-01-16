"""
A module that deals with business, products and
service reviews
"""
from flask import Blueprint, jsonify, request, abort
from flask_login import current_user
from flask_jwt_extended import jwt_required
from services.reviews import ReviewService
from models.review import Review

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('/create-reviews', methods=['POST'])
@jwt_required()
def create_review():
    """Create a new review.
    This endpoint allows authenticated users to create a new review.
    A review must include a `comment` and a `rating` between 1 and 5.

    Returns:
        JSON response containing the created review details.
        HTTP Status Code:
            - 201: Review created successfully.
            - 400: Missing fields or invalid rating.
    """
    data = request.get_json()

    # Validate required fields.
    if 'comment' not in data or 'rating' not in data:
        abort(400, description="Missing required fields: comment and rating")

    # Ensure the rating is between 1 and 5
    if rating < 1 or rating > 5:
        abort(400, description='Rating must be between 1 and 5')

    comment = data['comment']
    rating = data['rating']
    product_id = data.get('product_id')
    service_id = data.get('service_id')

    review, error = ReviewService.create_review(
        comment, rating, current_user.id, product_id, service_id
        )

    if error:
        return jsonify({'message': error}), 400

    return jsonify({
        'id': review.id,
        'comment': review.comment,
        'rating': review.rating,
        'created_at': review.created_at
    }), 201


@review_bp.route(
        '/get-reviews/<string:review_type>/<int:item_id>',
        methods=['GET'])
def get_reviews(review_type, item_id):
    """Retrieve reviews for a specific product or service.
    Args:
        review_type (str): The type of the item ('product' or 'service').
        item_id (int): The ID of the product or service.
        reviews_list(list): list of reviews

    Returns:
        JSON response containing a list of reviews.
    """
    reviews = []

    if review_type == 'product':
        reviews = ReviewService.get_reviews_by_product(item_id)
    elif review_type == 'service':
        reviews = ReviewService.get_reviews_by_service(item_id)
    else:
        return jsonify(
            {
                'message': 'Invalid review type. Use "product" or "service".'
             }), 400

    if not reviews:
        return jsonify(
            {
                'message': f'No reviews found for this {review_type}.'
             }), 404

    reviews_list = [{
        'id': review.id,
        'user': review.user.username if review.user else 'Unknown',
        'comment': review.comment,
        'rating': review.rating,
        'review_date': review.created_at
    } for review in reviews]

    return jsonify({'reviews': reviews_list}), 200


@review_bp.route('/update-reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update an existing review.
    This endpoint allows authenticated users to update their own reviews.
    Only `comment` and `rating` fields can be updated.

    Args:
        review_id (int): The ID of the review to be updated.

    Returns:
        JSON response containing the updated review details.
        HTTP Status Code:
            - 200: Review updated successfully.
            - 400: Invalid rating.
            - 403: User is not authorized to update this review.
    """
    data = request.get_json()
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        return jsonify(
            {
                'message': 'You can only edit your own reviews.'
             }), 403

    updated_review, error = ReviewService.update_review(
        review,
        comment=data.get('comment'),
        rating=data.get('rating')
    )

    if error:
        return jsonify({'message': error}), 400

    return jsonify({
        'id': updated_review.id,
        'comment': updated_review.comment,
        'rating': updated_review.rating,
        'created_at': updated_review.created_at
    }), 200


@review_bp.route('/delete-reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete an existing review.
    This endpoint allows authenticated users to delete their own reviews.

    Args:
        review_id (int): The ID of the review to be deleted.

    Returns:
        JSON response indicating success or failure.
        HTTP Status Code:
            - 200: Review deleted successfully.
            - 403: User is not authorized to delete this review.
    """
    review:Review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        return jsonify({'message': 'You can only delete your own reviews.'}), 403

    review, error = ReviewService.delete_review(review)

    if error:
        return jsonify({'message': error}), 400

    return jsonify({'message': 'Review deleted successfully.'}), 200
