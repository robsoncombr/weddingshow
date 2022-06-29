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


# TODO: important...
# I have decided to controle the user access based on an array/list of users/emails
# The correct approach should be to send an invitation to user, that accepts or deny it after registration, if accepted the user's id should be the foreign key for the wedding acl record.
class Wedding(Base):
    meta = {'collection': 'weddings'}
    user = db.ReferenceField(User)  # owner of the wedding
    name = db.StringField(required=True)
    # list of users with access to the wedding, format: {'email':String, 'is_admin':Boolean}
    users = db.ListField()


class Image(Base):
    meta = {'collection': 'images'}
    wedding = db.ReferenceField(Wedding)
    user = db.ReferenceField(User)
    id_approved = db.BooleanField(required=True, default=False)
    image_path = db.StringField(required=True)

# small tests - development only
# print(User(email="r@r.r",dt_updated=datetime.utcnow()).save())
#print(Wedding(name="Marriage", dt_updated=datetime.utcnow()).save())
#print(File(wedding="62baf6fb4080c418a7064260", dt_updated=datetime.utcnow()).save())
