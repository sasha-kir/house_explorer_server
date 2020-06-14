from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
BCRYPT_LOG_ROUNDS = 15

db = SQLAlchemy()
