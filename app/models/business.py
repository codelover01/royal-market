from . import db
from .baseModel import BaseModel
from sqlalchemy.exc import IntegrityError
from models.users import User


class Business(BaseModel):
    """A business model class that inherites from BaseModel"""
    name = db.Column(
        db.String(255),
        nullable = False,
        unique = True
        )
    email = db.Column(
        db.String(255),
        nullable = False,
        unique = True
        )
    description = db.Column(
        db.Text,
        nullable = False
    )
    location = db.Column(
        db.String(255),
        nullable = False
    )
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable = False
    )
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable = True)
    online_available = db.Column(
        db.Boolean,
        default=True
        )
    offline_available = db.Column(
        db.Boolean,
        default=True
        )
    
    # Relationships
    user = db.relationship('User', back_populates='business')
    product = db.relationship('Product', back_populates='business')
    services= db.relationship('Service', back_populates='business')
    reviews = db.relationship('Review', back_populates='business')

    @staticmethod
    def create_business(data: dict, current_user: User) -> tuple[dict, int]:
        """ Creates a new business 
        Args:
            - data (): Data entered by user to create a new business
            (e.g., name, email, owner_id, description of business, location,
            online_available, offline_available)
            - current_user (): The currently authenticated user.
        Returns:
            tuple[dict, int]: A response dictionary and HTTP status code.
            A newly created business on success
            Raises IntegrityErrors, keyErrors or Exception errors on failure.
        """
        try:
            new_business = Business(
                name = data.get('name'),
                email = data.get('email'),
                owner_id = current_user.id,
                description = data.get('description'),
                location = data.get('location'),
                online_available = data.get('online_available'),
                offline_available = data.get('offline_available')
            )
            new_business.save()
            return new_business
        
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig) if hasattr(e, 'orig') else ''
            
            if 'Duplicate entry' in error_message:
                if 'for key \'business.name\'' in error_message:
                    raise BusinessException(
                        message = 'Business name already exists. Please choose a different name',
                        code = 400,
                        field = 'name'
                    )
                if 'for key \'business.email\'' in error_message:
                    raise BusinessException(
                        message = 'Business email already exists. Please choose a different email.',
                        code = 400,
                        field = 'email'
                    )
            raise BusinessException(
                message = 'A database integrity error occurred.',
                code = 500,
                details = {'error_info': error_message}
            )

        except KeyError as e:
            raise BusinessException(
                message = 'Missing required field.',
                code = 400,
                details = {'KeyError_info': {str(e)}}
            )
        except Exception as e:
            raise BusinessException(
                message = 'An unexpected error occurred.',
                code = 500,
                details = {'error_info': {str(e)}}
            )


class BusinessException(Exception):
    """ Custom exception for business-specific errors. """
    def __init__(self, message:str, code: int = 400, field: str = None, details: dict = None):
        """
        Initialize a BusinessException.

        Args:
            message (str): A human-readable error message
            code (int): HTTP status code associated with the error.
            field (str): The field causing the error (e.g., 'name' or 'email')
            details (dict, optional): Additional details about the error
        """

        self.message = message
        self.code = code
        self.field = field
        self.details = details
        super().__init__(self.message)

    def to_dict(self):
        """
        Converts exception details into a dicionary for API responses
        """

        error_data = {
            'error': self.message,
            'code': self.code
        }

        if self.field:
            error_data['field'] = self.field
        if self.details:
            error_data['details'] = self.details
        return error_data
    
    def __str__(self):
        """
        String representation of the exception.
        """
        base_message = f'{self.code}: {self.message}'
        if self.field:
            base_message += f'(Field: {self.field})'
        return base_message


