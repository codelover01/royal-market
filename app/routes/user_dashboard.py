"""
A module that deals with user dashboard
operations.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.userService import UserService

user_dashboard_bp = Blueprint(
    'user_dashboard', __name__, url_prefix='/user')


@user_dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    """Retrieve user dashboard overview"""
    user_id = get_jwt_identity()  # Retrieve the user ID from the JWT token
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@user_dashboard_bp.route('/dashboard/orders', methods=['GET'])
@jwt_required()
def user_orders():
    """Fetch user orders"""
    user_id = get_jwt_identity()
    try:
        orders = UserService.get_user_orders(user_id)
        return jsonify([{
            "id": order.id,
            "product_name": order.product_name,
            "quantity": order.quantity,
            "status": order.status,
            "order_date": order.order_date.strftime('%Y-%m-%d')
        } for order in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_dashboard_bp.route('/dashboard/cart', methods=['GET'])
@jwt_required()
def user_cart():
    """Fetch user cart details"""
    user_id = get_jwt_identity()
    try:
        cart = UserService.get_user_cart(user_id)
        return jsonify([{
            "id": item.id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "price": item.price,
            "status": item.status
        } for item in cart]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_dashboard_bp.route('/dashboard/profile', methods=['GET', 'PUT'])
@jwt_required()
def user_profile():
    """Fetch or update user profile"""
    user_id = get_jwt_identity()
    
    if request.method == 'GET':
        try:
            user = UserService.get_user_by_id(user_id)
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        try:
            user = UserService.update_user(user_id, data)
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

@user_dashboard_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    """ Updates the user's data"""
    data = request.get_json()
    user_id = get_jwt_identity()  # Assumes you use jwt_required() for authentication
    try:
        user = UserService.update_user(
            user_id, 
            username=data.get('username'), 
            email=data.get('email'), 
            password=data.get('password')
        )
        return jsonify({
            "message": "User updated successfully.",
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Delete user (requires JWT)
@user_dashboard_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    """ Deletes the user """
    user_id = get_jwt_identity()
    try:
        result = UserService.delete_user(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
