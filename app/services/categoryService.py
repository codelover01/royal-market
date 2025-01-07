from models.category import Category

class CategoryService:
    @staticmethod
    def create_category(name, description=None):
        """Create a new category."""
        return Category.create_category(name, description)

    @staticmethod
    def get_category_by_id(category_id):
        """Retrieve a category by ID."""
        return Category.get_category_by_id(category_id)

    @staticmethod
    def get_all_categories():
        """Retrieve all categories."""
        return Category.get_all_categories()

    @staticmethod
    def update_category(category_id, name=None, description=None):
        """Update a category."""
        return Category.update_category(category_id, name, description)

    @staticmethod
    def delete_category(category_id):
        """Delete a category."""
        return Category.delete_category(category_id)

    @staticmethod
    def list_category_products(category_id):
        """List products in a category."""
        category = Category.get_category_by_id(category_id)
        return category.list_products()

    @staticmethod
    def list_category_services(category_id):
        """List services in a category."""
        category = Category.get_category_by_id(category_id)
        return category.list_services()

    @staticmethod
    def list_category_businesses(category_id):
        """List businesses in a category."""
        category = Category.get_category_by_id(category_id)
        return category.list_businesses()
    