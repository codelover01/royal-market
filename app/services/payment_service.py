"""
A module that deals with payment services
"""
from models.payment import Payment
from models.orders import Order
from models import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone


class PaymentService:
    """
    Service to handle payment-related business logic.
    """
    
    @staticmethod
    def create_payment(order_id, payment_method, payment_amount):
        """
        Create a payment entry for an order.
        """
        try:
            order:Order = Order.get_by_id(order_id)
            if not order:
                return {"error": "Order not found"}, 404

            if order.payment_status == 'paid':
                return {"error": "Order is already paid"}, 400

            payment = Payment(
                order_id=order_id,
                payment_date=datetime.now(timezone.utc),
                payment_method=payment_method,
                payment_amount=payment_amount,
                payment_status='paid'
            )

            order.payment_status = 'paid'
            db.session.add(payment)
            db.session.commit()

            return {
                "message": "Payment successful", "payment_id": payment.id
                }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_payment_by_id(payment_id):
        """
        Retrieve a payment by ID.
        """
        payment = Payment.get_by_id(payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404
        return payment

    @staticmethod
    def get_all_payments():
        """
        Retrieve all payments.
        """
        payments = Payment.query.all()
        return payments

    @staticmethod
    def refund_payment(payment_id):
        """
        Process a refund for a payment.
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return {"error": "Payment not found"}, 404

            if payment.payment_status == 'refunded':
                return {"error": "Payment already refunded"}, 400

            payment.payment_status = 'refunded'
            db.session.commit()

            return {"message": "Payment refunded successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
