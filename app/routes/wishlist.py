# routes/api_wishlist.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from services.wishlist import WishlistService

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@wishlist_bp.route('/get-wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """Get all items in the user's wishlist (products and services)."""
    wishlist_items:WishlistService = WishlistService.find_by_user(current_user.id)
    if not wishlist_items:
        return jsonify({'message': 'Your wishlist is empty.'}), 404

    result = []
    for item in wishlist_items:
        item_data = {
            'id': item.id,
            'user_id': item.user_id,
        }
        if item.product:
            item_data['product'] = {
                'id': item.product.id,
                'name': item.product.name,
                'description': item.product.description
            }
        if item.service:
            item_data['service'] = {
                'id': item.service.id,
                'name': item.service.name,
                'description': item.service.description
            }
        result.append(item_data)

    return jsonify({'wishlist': result}), 200

@wishlist_bp.route('/add', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add a product or service to the wishlist."""
    data = request.get_json()
    product_id = data.get('product_id')
    service_id = data.get('service_id')

    if not product_id and not service_id:
        return jsonify({'message': 'Either product_id or service_id must be provided.'}), 400

    item = WishlistService.add_to_wishlist(current_user.id, product_id, service_id)
    
    item_data = {
        'id': item.id,
        'user_id': item.user_id,
    }
    
    if item.product:
        item_data['product'] = {
            'id': item.product.id,
            'name': item.product.name,
            'description': item.product.description
        }
    
    if item.service:
        item_data['service'] = {
            'id': item.service.id,
            'name': item.service.name,
            'description': item.service.description
        }

    return jsonify({
        'message': 'Product/Service added to your wishlist.',
        'wishlist_item': item_data
    }), 201

@wishlist_bp.route('/remove', methods=['POST'])
@login_required
def remove_from_wishlist():
    """Remove a product or service from the wishlist."""
    data = request.get_json()
    product_id = data.get('product_id')
    service_id = data.get('service_id')

    if not product_id and not service_id:
        return jsonify({'message': 'Either product_id or service_id must be provided.'}), 400

    item = WishlistService.remove_from_wishlist(current_user.id, product_id, service_id)
    if not item:
        return jsonify({'message': 'Product/Service not found in your wishlist.'}), 404

    return jsonify({'message': 'Product/Service removed from your wishlist.'}), 200
