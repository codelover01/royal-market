"""
A module that deals with inventory service code
"""
from models.inventory import Inventory
from models import db
from sqlalchemy.exc import SQLAlchemyError


class InventoryService:
    """Service layer for handling Inventory-related operations."""

    @staticmethod
    def add_inventory(item_id, product_id, service_id, stock):
        """
        Add a new inventory entry.

        Args:
            product_id (int): ID of the product.
            service_id (int): ID of the service.
            stock (int): Available stock.

        Returns:
            dict: Success or error message.
        """
        try:
            if item_id == 'product_id':
                inventory = Inventory(
                    product_id = product_id,
                    stock = stock
                )
            elif item_id == 'service_id':
                inventory = Inventory(
                service_id=service_id,
                stock=stock
                )
                inventory.save()
                return {
                    "message": "Inventory added successfully",
                    "id": inventory.id
                    }
            else:
                return {"message": ""}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def get_inventory_by_id(inventory_id):
        """
        Retrieve an inventory record by its ID.

        Args:
            inventory_id (int): Inventory record ID.

        Returns:
            Inventory | dict: Inventory object or error message.
        """
        inventory = Inventory.get_by_id(inventory_id)
        if not inventory:
            return {"error": "Inventory not found"}
        return inventory

    @staticmethod
    def get_all_inventory():
        """
        Retrieve all inventory records.

        Returns:
            list: List of inventory records.
        """
        return Inventory.get_all()

    @staticmethod
    def update_stock(inventory_id, stock):
        """
        Update the stock of an inventory record.

        Args:
            inventory_id (int): Inventory record ID.
            stock (int): Updated stock count.

        Returns:
            dict: Success or error message.
        """
        inventory:Inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {"error": "Inventory not found"}
        try:
            inventory.stock = stock
            inventory.update()
            return {"message": "Stock updated successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def delete_inventory(inventory_id):
        """
        Delete an inventory record.

        Args:
            inventory_id (int): Inventory record ID.

        Returns:
            dict: Success or error message.
        """
        inventory:Inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {"error": "Inventory not found"}
        try:
            inventory.delete()
            return {"message": "Inventory deleted successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}
