from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from . import db, bcrypt


class Auth(db.Model):
    __tablename__ = "auth"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.LargeBinary(60), nullable=False)

    def __init__(self, email, plaintext_password):
        self.email = email
        self.password = plaintext_password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)
