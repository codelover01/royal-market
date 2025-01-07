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
    return jsonify(result)


# Get Payment by ID
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    result = PaymentService.get_payment_by_id(payment_id)
    if isinstance(result, dict):
        return jsonify(result), 404
    return jsonify({
        "id": result.id,
        "order_id": result.order_id,
        "payment_date": result.payment_date,
        "payment_method": result.payment_method,
        "payment_amount": result.payment_amount,
        "payment_status": result.payment_status
    })


# Get All Payments
@payment_bp.route('/', methods=['GET'])
def get_all_payments():
    payments = PaymentService.get_all_payments()
    result = [{
        "id": payment.id,
        "order_id": payment.order_id,
        "payment_date": payment.payment_date,
        "payment_method": payment.payment_method,
        "payment_amount": payment.payment_amount,
        "payment_status": payment.payment_status
    } for payment in payments]
    return jsonify(result)


# Refund Payment
@payment_bp.route('/refund/<int:payment_id>', methods=['POST'])
def refund_payment(payment_id):
    result = PaymentService.refund_payment(payment_id)
    return jsonify(result)
