import pytest

from explorer_api import create_app

from explorer_api.models import db
from explorer_api.models.User import User
from explorer_api.models.Auth import Auth


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(testing=True)

    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    context = flask_app.app_context()
    context.push()

    yield testing_client

    context.pop()


@pytest.fixture(scope="module")
def init_database():
    db.drop_all()
    db.create_all()

    # Insert user data
    test_email = "test@test.com"
    user = User(username="test", email=test_email)
    user_auth = Auth(email=test_email, plaintext_password="secret")
    db.session.add(user)
    db.session.add(user_auth)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.close()
    db.drop_all()
