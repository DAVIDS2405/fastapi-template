from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()

username = os.environ.get('NEONDB_USER')
password = os.environ.get('NEONDB_PASSWORD')
host = os.environ.get('NEONDB_HOST')
database = os.environ.get('NEONDB_DATABASE')

connection_string = URL.create(
    drivername="postgresql",
    username=username,
    password=password,
    host=host,
    database=database
)

engine = create_engine(
    connection_string,
    connect_args={'sslmode': 'require'}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
