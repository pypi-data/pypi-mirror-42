from mongoengine import NotUniqueError
from werkzeug.exceptions import HTTPException

SECRET_KEY = '<secret_key>'

MONGODB_DB = '<db_name>'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = '<username>'
MONGODB_PASSWORD = '<password>'

SOCKET_ACTIVE = True

USER_MODEL = 'models.user.User'
SESSION_MODEL = 'models.session.Session'

DEBUG = True

HANDLED_ERRORS = [
    HTTPException,
    Exception
]

ERROR_MAPPINGS = [
    (NotUniqueError, 400)
]
