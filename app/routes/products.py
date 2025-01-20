from flask import Blueprint, request, jsonify, redirect, url_for, Response
from flask_jwt_extended import get_current_user
from models.products import Product
from models.business import Business

products_bp = Blueprint("products", __name__, url_prefix='/products')

@products_bp.route("/add_products", methods=["POST"])
def add_product():
    """ Adds the product to the database.
    Args:
        owner_id: ID of the current business owner
        business_id: Business ID
        name: product name
        description: product descripion
        price: product price
        quantity: number of products added

    Returns:
        - Response(Status code: 403): If current user owns no business
        - Response(Status code: 400): if data got is invalid JSON
        - Response(Status code: 400): If the business ID is not got or provided.
        - Response(Status code: 403): if the Business ID is invalid or
        Current user owns no business.
        - Response(Status code: 201): On successful creation of the product.
        - Response(Status code: 500): for any related database errors.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    current_user = get_current_user()

    # Fetch businesses for the current user
    businesses = Business.find_by_attributes(owner_id=current_user.id)
    if not businesses:
        return jsonify({"error:", "You do not own any business"}), 403
    
    # Validate Business ID from JSON payload
    business_id = data.get('business_id')
    if not business_id:
        return jsonify({"error:", "Business ID is required."}), 400
    
    # Validate that the business exists and belongs to the current user
    business = Business.find_first_object(id=business_id, owner_id=current_user.id)
    if not business:
        return jsonify({"error:", "Invalid business ID or you do not own this business."}), 403
    
    try:
        product = Product(
            name = data["name"],
            description = data.get("description", ""),
            price = data["price"],
            quantity = data['quantity'],
            stock = data['stock'],
            business_id = business.id
        )
        product.save()
        return jsonify({
            "message": "Product added successfully",
            "product": product.to_dict()
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@products_bp.route("/list_products", methods=["GET"])
def list_products():
    """ Endpoint to list all products
    Gets all the products
    Returns:
        - Response(Status code: 200) for all the products related to 
        the current user's business.
        - Response(Status code: 500) for any database related errors.
    """
    try:
        # Fetch the products
        products: Product = Product.get_all()  # Using BaseModel's get_all method
        return jsonify({"products": [products.to_dict() for product in products]}), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@products_bp.route(
        '/delete_products/<int:product_id>', methods = ['POST', 'DELETE'])
def delete_product(product_id) -> Response:
    """ Endpoint to delete a specific service by ID.
    Args:
        - product_id: ID of product to delete
        - id: ID of business which the product belongs to.
    Returns:
        Response(Status code: 403): If product does not belong to the current user.
        Response(Status code: 200): On successful deletion of the product.
        Response(Status code: 500) for any database related errors.
    """
    try:
        # Fetch the product
        product: Product = Product.get_or_404(product_id)

        current_user = get_current_user()

        # Ensure the product belons to the current user
        business = Business.find_first_object(
            id = product.business_id, owner_id = current_user.id
            )
        if not business:
            return jsonify({
                "error": "Unauthorized: You don not own this product."
                }), 403
        
        # Perform the delete
        product.delete()
        return jsonify({
            "messaage": "Product deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500