from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.categoryService import CategoryService

category_bp = Blueprint('category', __name__, url_prefix='/categories')

# Create Category
@category_bp.route('/create', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    try:
        category = CategoryService.create_category(name, description)
        return jsonify({"id": category.id, "name": category.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Get All Categories
@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all_categories()
    return jsonify([{"id": cat.id, "name": cat.name} for cat in categories]), 200

# Get Category by ID
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = CategoryService.get_category_by_id(category_id)
    return jsonify({"id": category.id, "name": category.name, "description": category.description}), 200

# Update Category
@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    category = CategoryService.update_category(category_id, name, description)
    return jsonify({"id": category.id, "name": category.name, "description": category.description}), 200

# Delete Category
@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    result = CategoryService.delete_category(category_id)
    return jsonify(result), 200

# List Category Products
@category_bp.route('/<int:category_id>/products', methods=['GET'])
def list_category_products(category_id):
    products = CategoryService.list_category_products(category_id)
    return jsonify([{"id": p.id, "name": p.name} for p in products]), 200
