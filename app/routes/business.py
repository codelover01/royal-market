from flask import Blueprint, request, jsonify
from flask_login import current_user
from flask_jwt_extended import jwt_required
from models.business import Business, BusinessException


business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/create_business', methods=['POST'], strict_slashes=False,
                   endpoint='create_business')
@jwt_required()
def create_business() -> tuple[dict[str, str], int]:
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

        # new_business: Business = Business.create_business(data, current_user)
        new_business: Business = Business.create_business(data)
        new_business.save()
        return jsonify({
                'message': 'Business created successfully',
                'New_business': new_business.to_dict()
                }), 201
    except BusinessException as e:
        # return jsonify({(e.to_dict()), e.code})
        return jsonify({"error": {str(e)}})
    
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred.', 'details': str(e)
            }), 500
    
@business_bp.route('/update_business/<int:business_id>', methods = ['PUT'],
                   endpoint='update_business')
@jwt_required
def update_business(business_id: int) -> tuple[dict[str, str], int]:
    """
    Handles the update of business credentials.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'message': 'Invalid JSON'
            }), 400

        business: Business = Business.get_or_404(business_id)
        if not business:
            return jsonify({'message': "Invalid Business ID"}), 400

        # Ensure ownership
        if business.owner_id != current_user.id:
            return jsonify({'error': 'Unauthorized: You do not own this business.'}), 403

        # Update fields
        business.name = data.get('name', business.name)
        business.email = data.get('email', business.email)
        business.description = data.get('description', business.description)
        business.location = data.get('location', business.location)
        business.online_available = data.get('online_available', business.online_available)
        business.offline_available = data.get('offline_available', business.offline_available)
        business.save()

        return jsonify({
            'Message': 'Business updated successfully.'
        }), 200

    except KeyError as e:
        raise BusinessException(
                message = 'Missing required field.',
                code = 400,
                details = {'KeyError_info': {str(e)}}
            )
    except Exception as e:
        raise BusinessException(
                message = 'An unexpected error occurred.',
                code = 500,
                details = {'error_info': {str(e)}}
            )

@business_bp.route('/delete_business/<int:business_id>', methods = ['DELETE'], strict_slashes = False,
                   endpoint='delete_business')
@jwt_required
def delete_business(business_id: int) -> tuple[dict[str, str], int]:
    """
    Deletes or remove a business from the database by it's ID
    """
    try:
        # Ensure the business belons to the current user
        business: Business = Business.find_first_object(
            id = business_id, owner_id = current_user.id
            )
        if not business:
            return jsonify({
                "error": "Unauthorized: You don not own this business."
                }), 403
        
        # Perform the delete
        business.delete()
        return jsonify({
            "messaage": "Business deleted successfully"
        }), 200
    except BusinessException as e:
        return jsonify({
            'error': e.message, 'details': e.details}), e.code
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@business_bp.route('/get_businessses', methods = ['GET'], strict_slashes = False,
                   endpoint='get_business')
@jwt_required
def get_business():
    """
    Gets all the businesses in the database according to the User_id
    """
    # Retrieve all the businesses that belong to the current user
    businesses = Business.find_by_attributes(owner_id = current_user.id)
    if not businesses:
        return jsonify({
            'message': 'No businesses found for your account'
        }), 404
    
    return jsonify([
        {
            'message': 'These are your business credentials.',
            'id': business.id,
            'name': business.name,
            'email': business.email,
            'description': business.description,
            'location': business.location,
            'online_available': business.online_available,
            'offline_available': business.offline_available,
            'created_at': business.created_at,
            'updated_at': business.update_at
            } for business in businesses]), 200