# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from datetime import datetime
# Define a base model for other database tables to inherit


class Base(db.Document):
    meta = {'abstract': True, 'allow_inheritance': True}
    dt_created = db.DateTimeField(required=True, default=datetime.utcnow())
    dt_updated = db.DateTimeField(required=True, default=datetime.utcnow())


class User(Base):
    meta = {'collection': 'users'}
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)


class Wedding(Base):
    meta = {'collection': 'weddings'}
    user = db.ReferenceField(User)
    name = db.StringField(required=True)


# TODO: important...
# I'm using the user's email as the relationship key for demonstration and due to the time constraints.
# The correct approach should be to send an invitation to user, that accepts or deny it after registration, if accepted the user's id should be the foreign key for the wedding acl record.
#
class WeddingAcl(Base):
    meta = {'collection': 'wedding_acls'}
    wedding = db.ReferenceField(Wedding)
    # user = db.ReferenceField(User)
    # decided to create the relation based on the e-mail only
    email_user = db.StringField(required=True)
    is_admin = db.BooleanField(required=True, default=False)


class File(Base):
    meta = {'collection': 'files'}
    wedding = db.ReferenceField(Wedding)

# small tests - development only
# print(User(email="r@r.r",dt_updated=datetime.utcnow()).save())
#print(Wedding(name="Marriage", dt_updated=datetime.utcnow()).save())
#print(File(wedding="62baf6fb4080c418a7064260", dt_updated=datetime.utcnow()).save())