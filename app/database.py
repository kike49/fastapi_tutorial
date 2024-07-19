from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from .config import settings

# Construct the Data Source Name (DSN) for PostgreSQL connection. Structure: postgresql://DATABASE_USERNAME:DATABASE_PASSWORD@DATABASE_HOSTNAME/DATABASE_NAME
dsn = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}"

# Create the SQLAlchemy engine using the DSN. This engine object will be used to interact with the PostgreSQL database
engine = create_engine(dsn)

# Create a configured "Session" class; sessionmaker is a factory in SQLAlchemy is used to interact with the database. It manages operations such as database queries, updates, and transactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our ORM models to inherit from; declarative_base() returns a new base class from which all mapped classes should inherit.
Base = declarative_base()

# Dependency that will be used in FastAPI routes. This function provides a database session to the request and ensures it's closed after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connect to the database without using SQL Alchemy (before in main.py, moved here just for doc purposes)
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='culocaca', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Successful database connection")
except Exception as error:
    print(f"Connection failed, the error was {error}")