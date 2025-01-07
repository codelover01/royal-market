""" A module that automates the database model tables' creation. """

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app
from models import db

def create_database_tables():
    """Create database tables based on the defined models."""

    with app.app_context():
        db.create_all()
        print('Database tables created.')


if __name__ == '__main__':
    create_database_tables()