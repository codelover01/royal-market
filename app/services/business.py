from flask import Blueprint, request, jsonify, Response
from flask_login import current_user, login_required
from models.business import Business, BuinsessException


business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/create_business', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create() -> tuple[dict[str, str], int]:
    """ Adds a new business to the database
    Args:
        data
    Returns:
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON.'
            }), 400

        new_business: Business = Business.create_business(data, current_user)
        new_business.save()
        return jsonify({
                'message': 'Business created successfully',
                'New_business': new_business.to_dict()
                }), 201
    except BuinsessException as e:
        return jsonify({(e.to_dict()), e.code})
    
@business_bp.route('/update_business', methods = ['GET','PUT', 'POST'])
def update():
    """
    Handles the update of business credentials.
    """
    pass


@business_bp.route('/delete_business', methods = ['DELETE', 'POST'], strict_slashes = False)
def delete():
    """
    Deletes or remove a business from the database
    """
    pass