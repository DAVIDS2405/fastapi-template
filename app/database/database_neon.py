from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get('NEONDB_USER')
password = os.environ.get('NEONDB_PASSWORD')
host = os.environ.get('NEONDB_HOST')
database = os.environ.get('NEONDB_DATABASE')

connection_string = f"postgresql://{username}:{password}@{host}/{database}"

meta = MetaData()
engine = create_engine(
    connection_string,
    connect_args={'sslmode': 'require'}
)
conn = engine.connect()
