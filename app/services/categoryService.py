from models.category import Category
from models import db

class CategoryService:
    """ Class representation of CategoryService"""
    @staticmethod
    def create_category(data):
        """Create a new category.
        Args:
            name(str): name of the category
            decription(str): decription of the category
        
        Return:

            The newly created category
        """
        name = data.get('name')
        description = data.get('description')
        if not name :
            raise ValueError('Name is required')
        if not description:
            raise ValueError('Description is required')
        
        new_category = Category(**data)
        new_category.save()
        return new_category

    @staticmethod
    def get_category_by_id(category_id):
        """Retrieve a category by ID."""
        return Category.get_by_id(category_id)

    @staticmethod
    def get_all_categories():
        """Retrieve all categories."""
        return Category.query.all()

    @staticmethod
    # def update_category(category_id, name=None, description=None):
    def update_category(category_id, **kwargs):
        """Update a category."""
        category = Category.query.get(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} does not exist.")
        
        for key, value, in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
            else:
                raise AttributeError(
                    f"'Category' object has no attribute '{key}'"
                    )
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id):
        """Delete a category."""
        category:Category = Category.get_or_404(category_id)
        db.session.delete(category)
        return category

    @staticmethod
    def list_category_products(category_id):
        """List products in a category."""
        category = Category.get_by_id(category_id)
        return category.list_products()

    @staticmethod
    def list_category_services(category_id):
        """List services in a category."""
        category = Category.get_by_id(category_id)
        return category.list_services()

    @staticmethod
    def list_category_businesses(category_id):
        """List businesses in a category."""
        category = Category.get_by_id(category_id)
        return category.list_businesses()
    