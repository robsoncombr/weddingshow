# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
import collections
from email.policy import default
from importlib.metadata import requires
from app import db
from datetime import datetime
# Define a base model for other database tables to inherit


class Base(db.Document):
    meta = {'abstract': True, 'allow_inheritance': True}
    # TODO: default=datetime.utcnow() does not work as I expected, it will always return the time from when the Model was built in memory, I have no time to find the workaround for this. I will handle it on runtime methods.
    dt_created = db.DateTimeField(required=True)
    dt_updated = db.DateTimeField(required=True)


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
    users = db.ListField(default=[])


class Image(Base):
    meta = {'collection': 'images'}
    wedding = db.ReferenceField(Wedding)
    user = db.ReferenceField(User)
    user_email = db.StringField(required=True)
    filename = db.StringField(required=True)
    mimetype = db.StringField(required=True)
    thumb = db.BinaryField(default=None)
    is_approved = db.BooleanField(required=True, default=False)
    # TODO: due to lack of time, I am choosing to save user reviews in a list, with identification and calculate the total on the front, this creates a privacy issue, as it is possible to see other users' reviews.
    ratings = db.ListField(default=[])
    messages = db.ListField(default=[])

# small tests - development only
# print(User(email="r@r.r",dt_updated=datetime.utcnow()).save())
#print(Wedding(name="Marriage", dt_updated=datetime.utcnow()).save())
#print(File(wedding="62baf6fb4080c418a7064260", dt_updated=datetime.utcnow()).save())
