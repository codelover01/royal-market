"""
A module that deals with payments in the business
"""
from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')


# Create a Payment
@payment_bp.route('/create', methods=['POST'])
def create_payment():
    """
    Create a new payment

    Args:
        data
        order_id(int): Order ID
        payment_method(str): method used for payment
        payment_amount(int): amount to be paid

    Return:
        - 400 status code for Invalid JSON data
        and missing required fields.
        - 200 status code for successful payment.
    """
    data = request.get_json()
    if not data:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    order_id = data.get('order_id')
    payment_method = data.get('payment_method')
    payment_amount = data.get('payment_amount')

    if not all([order_id, payment_method, payment_amount]):
        return jsonify({"error": "Missing required fields"}), 400

    result = PaymentService.create_payment(order_id, payment_method, payment_amount)
    return jsonify({"Payment successful.": result}), 200


# Get Payment by ID
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """
    Get payment by it's payment ID
    Args:
        - payment_id(int): payment ID
    Returns:
        - JSON response with 200 status code
    """
    result = PaymentService.get_payment_by_id(payment_id)
    if isinstance(result, dict):
        return jsonify({"Payment details.":result}), 404
    return jsonify({
        "id": result.id,
        "order_id": result.order_id,
        "payment_date": result.payment_date,
        "payment_method": result.payment_method,
        "payment_amount": result.payment_amount,
        "payment_status": result.payment_status
    }), 200


# Get All Payments
@payment_bp.route('/', methods=['GET'])
def get_all_payments():
    """
    Gets all the payments.
    Args:
        - payments: payments in the database.
        - result(list): list of all payments.
    Returns:
        - A list of payments with status code 200
        - 404 status code for no payments found
    """
    try:
        payments = PaymentService.get_all_payments()
        if not payments:
            return jsonify({"error": "Not payments were found"}), 404
        result = [{
            "id": payment.id,
            "order_id": payment.order_id,
            "payment_date": payment.payment_date,
            "payment_method": payment.payment_method,
            "payment_amount": payment.payment_amount,
            "payment_status": payment.payment_status
        } for payment in payments]
        return jsonify({"Payments found":result}), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Refund Payment
@payment_bp.route('/refund/<int:payment_id>', methods=['POST'])
def refund_payment(payment_id):
    """
    Processes payment refund
    Args:
        - payment_id(int): payment ID
    Returns:
        - Successful payment refund with status code 200
    """
    result = PaymentService.refund_payment(payment_id)
    if not result:
        return jsonify({
            "error": "Payment ID missing or Invalid"
        }), 400
    return jsonify({
        "Successful payment refund.": result
        }), 200
