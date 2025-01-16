"""
A module that deals with review service
"""
from models import db
from models.review import Review

class ReviewService:
    @staticmethod
    def create_review(comment, rating, user_id, product_id=None, service_id=None):
        """Create a new review for a product or service.
        Args:
            - comment(str): user's comment
            - rating(int): users' rating between 1 and 5
            - user_id(int): user's ID
            - product_id(int): product ID
            - service_id(int): service ID
            - review(obj): the review object
        Returns:
            - Successful review
            - None
            - Any other exception errors.
        """
        try:

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
        except Exception as e:
            return (str(e))

    @staticmethod
    def get_reviews_by_product(product_id):
        """Fetch reviews for a product.
        Args:
            - product_id(int): product ID
        Returns:
            - All the reviews for a specific product by ID
        """
        return Review.query.filter_by(product_id=product_id).all()

    @staticmethod
    def get_reviews_by_service(service_id):
        """Fetch reviews for a service.
        Args:
            - service_id(int): service ID
        Returns:
            - All the reviews for a specific service by ID.
        """
        return Review.query.filter_by(service_id=service_id).all()

    @staticmethod
    def update_review(review, comment=None, rating=None):
        """Update an existing review.
        Args:
            - comment(str): user comment
            - review(str): user review
            - rating(int):  users' rating between 1 and 5
        Returns:
            - Successful review or None.
        """
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
