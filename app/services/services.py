from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user
from models.business import Business
from models.services import Service

services_bp = Blueprint('services', __name__, url_prefix='/services')


@services_bp.route("/add_services", methods=["POST"])
def add_service():
    """ Endpoint that handles addition of services
    Args:
        - owner_id: ID of the current business owner
        - business_id: Business ID to which the service belongs.
        - name: service name
        - description: service description
        - hourly_cost: service cost or price per hour
        - duration: how long the service lasts or takes place
    Returns:
        - Response(Status code: 400) for invalid JSON data.
        - Response(Status code: 403) if Current user owns no business
        - Response(Status code: 400) if Business ID is missing or not provided.
        - Response(Status code: 403) for invalid Business ID or current user
        does not own this particular business.
        - Response(Status code: 201) on successful service creation
        - Response(Status code: 500) for any database related errors.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
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
        new_service = Service(
            name=data["name"],
            description=data.get("description", ""),
            hourly_cost=data["hourly_cost"],
            duration = data["duration"],
            business_id = business.id
        )
        new_service.save()  # Using BaseModel's save method
        return jsonify({
            "message": "Service added successfully",
            "New Service": new_service.to_dict()
            }), 201
    # except IntegrityError as e:
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@services_bp.route("/list_services", methods=["GET"])
def list_services():
    """ Endpoint that handles listing of all services """
    services: Service = Service.get_all()  # Using BaseModel's get_all method
    return jsonify({
        "Services": [services.to_dict() for service in services]
        }), 200

@services_bp.route('/delete_services/<int:service_id>', methods=['POST','DELETE'])
def delete_service(service_id):
    """Endpoint to delete a specific service by ID."""
    try:
        # Fetch the service
        service: Service = Service.get_or_404(service_id)

        # Ensure the service belongs to the current user
        business = Business.find_first_object(id = service.business_id, owner_id = current_user.id)
        if not business:
            return jsonify({
                "error": "Unauthorized: You don't own this service."
                }), 403
        # Perform the delete
        service.delete()
        return jsonify({
        "message": "Service deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500