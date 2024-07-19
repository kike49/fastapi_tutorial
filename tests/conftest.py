from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db
from app.models import Base
import psycopg2
import pytest
from app.oauth2 import create_access_token
from app import models

# TEST DATABASE SETTINGS

# Function to create the testing database if it doesn't exist
def create_test_database(dsn, database_name):
    default_dsn = dsn.rsplit('/', 1)[0] + "/postgres" # Strip off the database name from the dsn to connect to the default postgres database: postgresql://username:password@hostname:port/postgres. It connects to the default postgres database to perform administrative tasks, such as creating a new database
    conn = psycopg2.connect(default_dsn)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {database_name}")
    cursor.close()
    conn.close()

# Database names for testing
test_db_name = f"{settings.DATABASE_NAME}_test"

# DSN for the test database
dsn = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{test_db_name}"

# Run the function to create the test database if it doesn't exist
create_test_database(dsn, test_db_name)

# Create the SQLAlchemy engine for the test database
engine = create_engine(dsn)

# Create a session factory bound to the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# FIXTURES: like reusable constants for our all our tests files

# Creates a session on the database
@pytest.fixture(scope="function") # This scope will make the fixture created only once at the beggining so it is not regenerated every test function that is called (that is the defaut behaviour by the function)
def session():
    # First we delete tables if any and create them so after the test they are still accesible to check
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the TestClient fror fastAPI
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Creates a test user
@pytest.fixture
def create_test_user(client):
    user_data = {"email": "correct_email@example.com", "password": "correctPassword"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Creates a 2nd test user
@pytest.fixture
def create_test_user2(client):
    user_data = {"email": "correct_email2@example.com", "password": "correctPassword2"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Creates a token for authentication validation of the created user above
@pytest.fixture
def create_token_test_user(create_test_user, client):
    login_data = {"username": create_test_user["email"], "password": create_test_user["password"]}
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

# Creates an authorized (logged in) client (user) for post requests
@pytest.fixture
def create_authorized_test_client(client, create_token_test_user):
    client.headers = {**client.headers, "Authorization": f"Bearer {create_token_test_user}"}
    return client

# Posts creation for testing purposes (test DB is empty) returns a query to access post properties in tests
@pytest.fixture
def create_test_posts(create_test_user, create_test_user2, session): # session is passed because we need to work with the DB
    post_data = [{
        "title": "1st test post title",
        "content": "Content for first test post",
        "owner_id": create_test_user["id"]
    }, {
        "title": "2nd test post title",
        "content": "Content for 2nd test post",
        "owner_id": create_test_user["id"]
    }, {
        "title": "3rd test post title",
        "content": "Content for 3rd test post",
        "owner_id": create_test_user["id"]
    }, {
        "title": "4th test post title",
        "content": "Content for 4th test post",
        "owner_id": create_test_user2["id"]
    }]

    def create_post_model(post_dict: dict): # Helper function to transform the list of dicts into a post schema
        return models.Post(**post_dict)
    
    post_list = list(map(create_post_model, post_data)) # To iterate on every post of the list a convert it into the post schema format and then keep them in a list
    session.add_all(post_list)
    session.commit()
    return post_list