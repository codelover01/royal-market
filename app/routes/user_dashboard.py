from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

user_dashboard_bp = Blueprint('user_dashboard', __name__, url_prefix='/user')

@user_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    """Retrieve user dashboard overview"""
    return jsonify({
        "message": "User Dashboard",
        "user": current_user.to_dict(),
        "recent_orders": [],  # Example data
        "cart_items": []
    })

@user_dashboard_bp.route('/dashboard/orders', methods=['GET'])
@login_required
def user_orders():
    """Fetch user orders"""
    orders = []  # Fetch orders from the database
    return jsonify({"orders": orders})

@user_dashboard_bp.route('/dashboard/cart', methods=['GET'])
@login_required
def user_cart():
    """Fetch user cart details"""
    cart = []  # Fetch cart from the database
    return jsonify({"cart": cart})

@user_dashboard_bp.route('/dashboard/profile', methods=['GET', 'PUT'])
@login_required
def user_profile():
    """Fetch or update user profile"""
    if request.method == 'GET':
        return jsonify(current_user.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        current_user.update(**data)
        return jsonify({"message": "Profile updated successfully"})
