# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from datetime import datetime
# Define a base model for other database tables to inherit


class Base(db.Document):
    meta = {'abstract': True, 'allow_inheritance': True}
    dt_created = db.DateTimeField(required=True, default=datetime.utcnow())
    dt_updated = db.DateTimeField(required=True)


class User(Base):
    meta = {'collection': 'users'}
    email = db.StringField(required=True)


class Wedding(Base):
    meta = {'collection': 'weddings'}
    name = db.StringField(required=True)


class WeddingAcl(Base):
    meta = {'collection': 'wedding_acls'}
    wedding = db.ReferenceField(Wedding)
    # user = db.ReferenceField(User)
    # decided to create the relation based on the e-mail only
    user_email = db.StringField(required=True)
    is_admin = db.BooleanField(required=True, default=False)


class File(Base):
    meta = {'collection': 'files'}
    wedding = db.ReferenceField(Wedding)

# small tests - development only
# print(User(email="r@r.r",dt_updated=datetime.utcnow()).save())
#print(Wedding(name="Casamento", dt_updated=datetime.utcnow()).save())
#print(File(wedding="62baf6fb4080c418a7064260", dt_updated=datetime.utcnow()).save())
