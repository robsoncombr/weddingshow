# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# default url prefix
# TODO: implement the default Blueprint
URL_PREFIX = '/api/v1'

# Define the SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_CONNECT_OPTIONS = {}
# /usr/local/lib/python3.10/site-packages/flask_sqlalchemy/__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# mongoengine definitions
MONGODB_SETTINGS = {
  'db':'weddingshow',
  'host':'weddingshow-mongo5',
  'port':27017
}

# websocket
SOCK_SERVER_OPTIONS = {'ping_interval': 25}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "fzgFxTZe3MgRax9V2K8y7KOSQHA9WRIVUeN4RVT9VdufoqlP1mMgxJwUwjenhZGSx3UUIvBmKNjaAWj1viMHbSOyo9uqcabS7Pb6c2Nsrgaf0fXEu80buJHr780omOIC"

# Secret key for signing cookies
SECRET_KEY = "NN3WNCWWY4TWwR3wIpUVWw3d9uuV8qEo1ipkAHxvr6mW6qpNw73xH5zs1ge6vF1h1iIUqjQlCFZXwuE8o4yE3RxUZB5KQEVZdA7KbAgyOAlUK8JtUbeActwV1yr0h8XU"