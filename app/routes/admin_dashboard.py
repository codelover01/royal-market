from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.users import User
from models.products import Product
from models.orders import Order

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    """Retrieve admin dashboard overview"""
    return jsonify({
        "message": "Admin Dashboard",
        "total_users": User.query.count(),
        "total_products": Product.query.count(),
        "pending_orders": Order.query.filter_by(status='pending').count()
    })

@admin_dashboard_bp.route('/dashboard/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    """View or add products"""
    if request.method == 'GET':
        products: Product = Product.find_by_attributes()
        return jsonify({"products": [p.to_dict() for p in products]})
    elif request.method == 'POST':
        data = request.get_json()
        new_product = Product(**data)
        new_product.save()
        return jsonify({"message": "Product added successfully"})

@admin_dashboard_bp.route('/dashboard/orders', methods=['GET'])
@login_required
def admin_orders():
    """View and manage orders"""
    orders = Order.query.all()
    return jsonify({"orders": [o.to_dict() for o in orders]})

@admin_dashboard_bp.route('/dashboard/users', methods=['GET'])
@login_required
def admin_users():
    """View all users"""
    users = User.query.all()
    return jsonify({"users": [u.to_dict() for u in users]})

@admin_dashboard_bp.route('/dashboard/analytics', methods=['GET'])
@login_required
def admin_analytics():
    """View analytics"""
    return jsonify({
        "sales_data": [],
        "user_growth": [],
    })
