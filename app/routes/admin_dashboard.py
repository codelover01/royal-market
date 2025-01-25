"""
A module that deals with admin operations.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from services.admin_service import AdminService
from routes.products import add_product, list_products
from routes.services import add_service, list_services
from services.order_service import OrderService


admin_dashboard_bp = Blueprint(
    'admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route(
        '/dashboard', methods=['GET'], endpoint='dashboard' )
@jwt_required()
def admin_dashboard():
    """Retrieve admin dashboard overview"""
    current_user = get_current_user()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    else:
        return jsonify({"Admin {current_user} are welcome"}), 200


@admin_dashboard_bp.route(
        '/dashboard/products', methods=['GET', 'POST'],
        endpoint='admin_products')
@jwt_required
def admin_products():
    """View or add products"""
    if request.method == 'GET':
        products = list_products()
        return jsonify([{
            "id": product.id,
            "name": product.name,
            "price": product.price
        } for product in products]), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({"error": "Invalid data"}), 400

        product = add_product(data['name'], data['price'])
        return jsonify({
            "message": "Product created successfully",
            "id": product.id,
            "name": product.name,
            "price": product.price
        }), 201


@admin_dashboard_bp.route(
        '/dashboard/services', methods=['GET', 'POST'],
        endpoint='admin_services')
@jwt_required
def admin_services():
    """View or add services"""
    if request.method == 'GET':
        services = list_services()
        return jsonify([{
            "id": service.id,
            "name": service.name,
            "price": service.price
        } for service in services]), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({"error": "Invalid data"}), 400

        service = add_service(data['name'], data['price'])
        return jsonify({
            "message": "Service created successfully",
            "id": service.id,
            "name": service.name,
            "price": service.price
        }), 201


@admin_dashboard_bp.route(
        '/dashboard/orders', methods=['GET'],
        endpoint='admin_orders')
@jwt_required
def admin_orders():
    """View all orders"""
    orders = OrderService.get_all_orders()

    if not orders:
        return jsonify({"error": "Invaild data"}), 400
    return jsonify([{
        "id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "date": order.date
    } for order in orders]), 200


@admin_dashboard_bp.route(
        '/dashboard/users', methods=['GET'],
        endpoint='admin_users')
@jwt_required
def admin_users():
    """View all users"""
    users = AdminService.get_all_users()
    if not users:
        return jsonify({
            "error": "Users not found."
        }), 404
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    } for user in users]), 200


@admin_dashboard_bp.route(
        '/dashboard/analytics', methods=['GET'],
        endpoint='admin_analytics')
@jwt_required
def admin_analytics():
    """View analytics"""
    pass

@admin_dashboard_bp.route('/dashboard/users/<int:user_id>', methods=['GET'])
@jwt_required()
def admin_user_detail(user_id):
    """Get a specific user details by ID"""
    try:
        user = AdminService.get_user_by_id(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@admin_dashboard_bp.route('/dashboard/users/<int:id>', methods=['PUT'])
@jwt_required()
def admin_update_user(id):
    """Update a user role"""
    data = request.get_json()
    new_role = data.get('role')
    if not new_role:
        return jsonify({"error": "Role is required"}), 400

    try:
        user = AdminService.update_user_role(id, new_role)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'email': user.email
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@admin_dashboard_bp.route('/dashboard/users/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(id):
    """Delete a user"""
    try:
        result = AdminService.delete_user(id)
        if not result:
            return jsonify({
                "error": "User not found"
            }), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
