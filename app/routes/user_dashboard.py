"""
A module that deals with user dashboard
operations.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

user_dashboard_bp = Blueprint(
    'user_dashboard', __name__, url_prefix='/user')


@user_dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    """Retrieve user dashboard overview"""
    pass


@user_dashboard_bp.route('/dashboard/orders', methods=['GET'])
@jwt_required()
def user_orders():
    """Fetch user orders"""
    pass


@user_dashboard_bp.route('/dashboard/cart', methods=['GET'])
@jwt_required()
def user_cart():
    """Fetch user cart details"""
    pass


@user_dashboard_bp.route('/dashboard/profile', methods=['GET', 'PUT'])
@jwt_required()
def user_profile():
    """Fetch or update user profile"""
    pass
