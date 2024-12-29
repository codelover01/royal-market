from flask import Flask
from . import db
from datetime import datetime, timezone


class BaseModel(db.Model):
    """Base class for all models, inherits from SQLAlchemy's Model class"""
    __abstract__ = True  # To avoid creating a table for BaseModel itself
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Define sensitive fields to exclude
    sensitive_fields = {"password", "secret_key"}

    def to_dict(self, serialize: bool = False) -> dict:
        """ Convert object to a dictionary representation """
        result = {}
        for key, value in self.__dict__.items():
            if key in self.sensitive_fields:  # Explicitly skip sensitive fields
                continue
            if not serialize and key[0] == '_':  # Skip private fields
                continue
            if isinstance(value, datetime):  # Format datetime fields
                result[key] = value.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                result[key] = value
        return result

    def save(self):
        """ Save current object to the database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Remove object from the database """
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """ Updates objects from the database """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' has no attribute {key}")
        db.session.commit()

    @classmethod
    def get_all(cls):
        """ Return all objects of this model """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id: str):
        """ Return one object by its ID """
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id: str):
        """ 
        Returns one object by its ID
        or status code 404 if not present
         """
        return cls.query.get_or_404(id)

    @classmethod
    def find_by_attributes(cls, attributes: dict):
        """ Search for objects that match the given attributes """
        filters = []
        for key, value in attributes.items():
            filters.append(getattr(cls, key) == value)
        return cls.query.filter(*filters).all()
    
    @classmethod
    def find_first_object(cls, attributes: dict):
        """ Search for the first object that match the given attributes """
        filters = []
        for key, value in attributes.items():
            if hasattr(cls, key):  # Ensure the attribute exists in the model
                filters.append(getattr(cls, key) == value)
            else:
                raise AttributeError(f"'{cls.__name__}' has no attribute '{key}'")
        return cls.query.filter(*filters).first()
    

    @classmethod
    def paginate(cls, page=1, per_page=10, filters=None):
        """ Generic pagination method 
        Args:
            -page: Current page number (default to 1)
            -per_page: Number of items per page(defaults to 10 items)
            -filters: Optional dictionary of attributes to filter the query.
            -meta: Includes pagination metadata 
            (current_page: current page,
            total_pages: total nmber of pages related to this filters,
            total_itms: total number of items related to this filters
            has_next: the page has next pages,
            has_prev: the page has previous pages.
            ).

        Return:
            Correctly Paginated data.
        """
        query = cls.query

        if filters:
            for key, value in filters.items():
                if hasattr(cls, key):
                    query = query.filter(getattr(cls, key) == value)
                else:
                    raise AttributeError(f"'{cls.__name__}' has no attribute '{key}'")
        
        paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "data": [item.to_dict() for item in paginated_data.items],
            "meta": {
                "current_page": paginated_data.page,
                "total_pages": paginated_data.pages,
                "total_items": paginated_data.total,
                "per_page": paginated_data.per_page,
                "has_next": paginated_data.has_next,
                "has_prev": paginated_data.has_prev
            }
        }
    