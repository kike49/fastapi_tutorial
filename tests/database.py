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

# Function to create the testing database if it doesn't exist
def create_test_database(dsn, database_name):
    # Strip off the database name from the dsn to connect to the default postgres database: postgresql://username:password@hostname/postgres. It connects to the default postgres database to perform administrative tasks, such as creating a new database
    default_dsn = dsn.rsplit('/', 1)[0] + "/postgres"
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
dsn = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{test_db_name}"

# Run the DB test creation function
create_test_database(dsn, test_db_name)

# Create the SQLAlchemy engine
engine = create_engine(dsn)

# Open session for test
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixures: like constants for our tests
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

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
