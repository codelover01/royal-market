from models import db

class ReviewService:
    @staticmethod
    def create_review(comment, rating, user_id, product_id=None, service_id=None):
        """Create a new review for a product or service."""
        if not (1 <= rating <= 5):
            return None, "Rating must be between 1 and 5."
        
        review = Review(
            comment=comment,
            rating=rating,
            user_id=user_id,
            product_id=product_id,
            service_id=service_id
        )
        db.session.add(review)
        db.session.commit()
        return review, None

    @staticmethod
    def get_reviews_by_product(product_id):
        """Fetch reviews for a product."""
        return Review.query.filter_by(product_id=product_id).all()

    @staticmethod
    def get_reviews_by_service(service_id):
        """Fetch reviews for a service."""
        return Review.query.filter_by(service_id=service_id).all()

    @staticmethod
    def update_review(review, comment=None, rating=None):
        """Update an existing review."""
        if comment:
            review.comment = comment
        if rating:
            if not (1 <= rating <= 5):
                return None, "Rating must be between 1 and 5."
            review.rating = rating
        db.session.commit()
        return review, None

    @staticmethod
    def delete_review(review):
        """Delete an existing review."""
        db.session.delete(review)
        db.session.commit()
        return True, None




from flask import request, jsonify, abort, Blueprint
from flask_login import current_user
from flask_jwt_extended import jwt_required
from models import db
from models.review import Review

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('/create-reviews', methods=['POST'])
@jwt_required()
def create_review():
    """
    Create a new review.

    This endpoint allows authenticated users to create a new review.
    A review must include a `comment` and a `rating` between 1 and 5.

    Returns:
        JSON response containing the created review details.
        HTTP Status Code:
            - 201: Review created successfully.
            - 400: Missing fields or invalid rating.
    """
    data = request.get_json()

    # Validate required fields
    if not data or 'comment' not in data or 'rating' not in data:
        abort(400, description="Missing required fields: comment and rating")

    comment = data['comment']
    rating = data['rating']

    # Ensure the rating is between 1 and 5
    if rating < 1 or rating > 5:
        abort(400, description="Rating must be between 1 and 5")

    new_review = Review(comment=comment, rating=rating, user_id=current_user.id)
    new_review.save()
    

    return jsonify({
        'id': new_review.id,
        'comment': new_review.comment,
        'rating': new_review.rating,
        'created_at': new_review.created_at
    }), 201


@review_bp.route('/get-reviews/<string:return_type>/<int:item_id>', methods=['GET'])
def get_reviews(review_type, product_id, service_id):
    """
    Retrieve all reviews for a specific product or service.

    Args:
        review_type (str): The type of the item ('product' or 'service').
        item_id (int): The ID of the product or service.

    Returns:
        JSON response containing a list of reviews.
    """
    if review_type == 'product':
        reviews: Review = Review.find_by_product(product_id)
    elif review_type == 'service':
        reviews = Review.find_by_service(service_id)
    else:
        return jsonify({
            'message': 'Invalid review type. Use "product" or "service".'
        }), 400

    if not reviews:
        return jsonify({'message': 'No reviews found for this {review_type}.'}), 404

    reviews_list = [{
        'id': review.id,
        'user': review.user.username if review.user else 'Unknown',
        'comment': review.comment,
        'rating': review.rating,
        'review_date': review.review_date
    } for review in reviews]
    return jsonify({'reviews': reviews_list}), 200

@review_bp.route('/update-reviews/<int:review_id>', methods=['PUT'], endpoint='update_review')
@jwt_required()
def update_review(review_id):
    """
    Update an existing review.

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
    review:Review = Review.get_or_404(review_id)

    # Check if the review belongs to the current user
    if review.user_id != current_user.id:
        return jsonify({'message': 'You can only edit your own reviews.'}), 403

    # Validate fields
    if 'comment' in data:
        review.comment = data['comment']
    if 'rating' in data:
        rating = data['rating']
        if rating < 1 or rating > 5:
            return jsonify({'message': 'Rating must be between 1 and 5.'}), 400
        review.rating = rating
    review.update()

    return jsonify({
        'id': review.id,
        'content': review.comment,
        'rating': review.rating,
        'created_at': review.created_at
    }), 200

@review_bp.route('/delete-reviews/<int:review_id>', methods=['DELETE'], endpoint='delete_review')
@jwt_required()
def delete_review(review_id):
    """
    Delete an existing review.

    This endpoint allows authenticated users to delete their own reviews.

    Args:
        review_id (int): The ID of the review to be deleted.

    Returns:
        JSON response indicating success or failure.
        HTTP Status Code:
            - 200: Review deleted successfully.
            - 403: User is not authorized to delete this review.
    """ 
    review:Review = Review.get_or_404(review_id)
    
    # Check if the review belongs to the current user
    if review.user_id != current_user.id:
        return jsonify({'message': 'You can only delete your own reviews.'}), 403
    review.delete()

    return jsonify({'message': 'Review deleted successfully.'}), 200
