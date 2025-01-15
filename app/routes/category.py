from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.categoryService import CategoryService

category_bp = Blueprint('category', __name__, url_prefix='/categories')

# Create Category
@category_bp.route('/create', methods=['POST'])
@jwt_required()
def create_category():
    """
    Create a new category
    Args:
        - data(dict): name and description of the category
    Returns:
        - Responses with status codes
        - 400 for Invalid JSON data.
        - 201 for successful category creation.
        - 400 for also any other related errors.
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "message": "Invalid JSON data."
            }), 400
    try:
        category = CategoryService.create_category(data)
        return jsonify(
            {
                "message": "Category successfully created.",
                "id": category.id,
                "name": category.name
             }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Get All Categories
@category_bp.route('/', methods=['GET'])
def get_categories():
    """
    Gets all the categories present
    Returns:
        - Jsonifies the response with 200 status code
    """
    categories = CategoryService.get_all_categories()
    return jsonify([{"id": cat.id, "name": cat.name} for cat in categories]), 200

# Get Category by ID
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Gets a single category by it's ID
    Args:
        - category_id(int): ID of the category
    Returns:
        - Jsonifies the specific category with status code 200
        - Otherwise it jsonifies any other related error.
    """
    try:
        category:CategoryService = CategoryService.get_category_by_id(category_id)
        return jsonify({"id": category.id, "name": category.name, "description": category.description}), 200
    except Exception as e:
        return jsonify({'error': {str(e)}})
# Update Category
@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """
    Updates the specific category based on it's ID
    Args:
        - category_id(int): ID of the category
        - name(str): name of the category
        - description of the category
    Returns:
        - Updates the category based on it's ID with status code 200
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided or Invalid JSON data"}), 400
    try:
        category = CategoryService.update_category(
            category_id,
            name = data.get('name'),
            description = data.get('description')
        )
        return jsonify({
            "id": category.id,
            "name": category.name,
            "description": category.description
        })
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except AttributeError as ae:
        return jsonify({"error": str(ae)}), 400

# Delete Category
@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """ Deletes a category from the database"""
    result = CategoryService.delete_category(category_id)
    return jsonify(result), 200

# List Category Products
@category_bp.route('/<int:category_id>/products', methods=['GET'])
def list_category_products(category_id):
    products = CategoryService.list_category_products(category_id)
    return jsonify([{"id": p.id, "name": p.name} for p in products]), 200
