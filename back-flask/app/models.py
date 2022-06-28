# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from datetime import datetime

# Define a base model for other database tables to inherit
class Base(db.Document):
    meta = {'abstract': True,'allow_inheritance': True}
    dt_created = db.DateTimeField(required=True, default=datetime.utcnow())
    dt_updated = db.DateTimeField(required=True)

class Wedding(Base):
    meta = {'collection': 'weddings'}

class File(Base):
    meta = {'collection': 'files'}
    wedding = db.ReferenceField(Wedding)