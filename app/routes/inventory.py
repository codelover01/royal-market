from flask import Blueprint, request, jsonify
from services.inventory_service import InventoryService

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


# Add Inventory
@inventory_bp.route('/add', methods=['POST'])
def add_inventory():
    """
    Add a new inventory entry.

    Args:
        Request JSON Payload:
        {
            "product_id": int, - product ID
            "service_id": int, - service ID
            "stock": int
        }

    Returns:
        JSON response confirming inventory creation.
    """
    data = request.get_json()
    product_id = data.get('product_id')
    service_id = data.get('service_id')
    stock = data.get('stock')

    if not all([product_id, service_id, stock]):
        return jsonify({"error": "Missing required fields"}), 400

    result = InventoryService.add_inventory(product_id, service_id, stock)
    return jsonify({result}), 201


# Get Inventory by ID
@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    """
    Retrieve an inventory record by its ID.

    Args:
        inventory_id (int): The ID of the inventory record.

    Returns:
        JSON response containing inventory details.
    """
    result = InventoryService.get_inventory_by_id(inventory_id)
    if isinstance(result, dict):
        return jsonify(result), 404
    return jsonify({
        "id": result.id,
        "product_id": result.product_id,
        "service_id": result.service_id,
        "stock": result.stock,
        "last_updated": result.last_updated
    })


# Get All Inventory
@inventory_bp.route('/', methods=['GET'])
def get_all_inventory():
    """
    Retrieve all inventory records.

    Returns:
        JSON response containing a list of all inventory records.
    """
    inventories = InventoryService.get_all_inventory()
    result = [{
        "id": inventory.id,
        "product_id": inventory.product_id,
        "service_id": inventory.service_id,
        "stock": inventory.stock,
        "last_updated": inventory.last_updated
    } for inventory in inventories]
    return jsonify(result)


# Update Inventory Stock
@inventory_bp.route('/update/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    """
    Update the stock of an inventory record.

    Request JSON Payload:
    {
        "stock": int
    }

    Returns:
        JSON response confirming stock update.
    """
    data = request.get_json()
    stock = data.get('stock')

    if stock is None:
        return jsonify({"error": "Stock value is required"}), 400

    result = InventoryService.update_stock(inventory_id, stock)
    return jsonify(result)


# Delete Inventory
@inventory_bp.route('/delete/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    """
    Delete an inventory record by ID.

    Args:
        inventory_id (int): The ID of the inventory record.

    Returns:
        JSON response confirming deletion.
    """
    result = InventoryService.delete_inventory(inventory_id)
    return jsonify(result)
