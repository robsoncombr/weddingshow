# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db, models
class User(models.Base):
    meta = {'collection': 'users'}
    email = db.StringField(required=True)
    is_admin = db.BooleanField(required=True, default=False)
