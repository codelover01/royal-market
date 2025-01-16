"""
A module that deals with admin operations.
"""
from flask import Blueprint, jsonify, request
from flask_login import current_user
from models.users import User
from models.products import Product
from models.orders import Order
from models.services import Service
from flask_jwt_extended import jwt_required


admin_dashboard_bp = Blueprint(
    'admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route(
        '/dashboard', methods=['GET'], endpoint='dashboard' )
@jwt_required()
def admin_dashboard():
    """Retrieve admin dashboard overview"""
    pass


@admin_dashboard_bp.route(
        '/dashboard/products', methods=['GET', 'POST'],
        endpoint='admin_products')
@jwt_required
def admin_products():
    """View or add products"""
    pass


@admin_dashboard_bp.route(
        '/dashboard/services', methods=['GET', 'POST'],
        endpoint='admin_services')
@jwt_required
def admin_services():
    """View or add services"""
    pass


@admin_dashboard_bp.route(
        '/dashboard/orders', methods=['GET'],
        endpoint='admin_orders')
@jwt_required
def admin_orders():
    """View and manage orders"""
    pass


@admin_dashboard_bp.route(
        '/dashboard/users', methods=['GET'],
        endpoint='admin_users')
@jwt_required
def admin_users():
    """View all users"""
    pass


@admin_dashboard_bp.route(
        '/dashboard/analytics', methods=['GET'],
        endpoint='admin_analytics')
@jwt_required
def admin_analytics():
    """View analytics"""
    pass