from models.orders import Order  # Assuming Order model is imported from models
from datetime import datetime

class OrderService:
    """
    Service class to handle order related operations.
    """

    @staticmethod
    def create_order(user_id, product_id, quantity, payment_status="pending"):
        """
        Create a new order.
        Args:
            - user_id (int): The ID of the user making the order.
            - product_id (int): The ID of the product being ordered.
            - quantity (int): The quantity of the product ordered.
            - payment_status (str): The current payment status of the order (default is "pending").
        Returns:
            - Order: The newly created order.
        """
        try:
            order = Order(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                order_date=datetime.utcnow(),
                payment_status=payment_status
            )
            order.save()  # Save the order to the database
            return order
        except Exception as e:
            raise ValueError(f"Failed to create order: {str(e)}")

    @staticmethod
    def get_order_by_id(order_id):
        """
        Retrieve an order by its ID.
        Args:
            - order_id (int): The ID of the order to retrieve.
        Returns:
            - Order: The order object.
        """
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found.")
        return order

    @staticmethod
    def get_all_orders():
        """
        Retrieve all orders.
        Returns:
            - list: List of all order objects.
        """
        orders = Order.query.all()
        return orders

    @staticmethod
    def update_order_status(order_id, status):
        """
        Update the payment status of an order.
        Args:
            - order_id (int): The ID of the order.
            - status (str): The new payment status (e.g., "paid", "pending", "cancelled").
        Returns:
            - Order: The updated order.
        """
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.payment_status = status
        order.save()  # Save the updated order status to the database
        return order

    @staticmethod
    def delete_order(order_id):
        """
        Delete an order from the database.
        Args:
            - order_id (int): The ID of the order to delete.
        Returns:
            - bool: True if the order was deleted, False otherwise.
        """
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.delete()  # Delete the order from the database
        return True
