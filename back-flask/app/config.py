# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# default url prefix
URL_PREFIX = '/api/v1'

# Define the SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_CONNECT_OPTIONS = {}

# TODO: WORK IN PROGRESS
# Define the Mongo database
MONGO_DATABASE_URI = 'mongodb://weddingshow-mongo5/'
MONGO_DATABASE_NAME = 'weddingshow'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"