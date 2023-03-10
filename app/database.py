import os
import json
from sqlalchemy import create_engine, inspect, MetaData, Table, Column
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SECRET_PATH = '/var/run/secrets/app/sensitive/sensitive'

if os.path.exists('/var/run/secrets/app/sensitive/sensitive'):
    f = open()
    credentials = json.load(f)
    f.close()
else:
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    credentials = {
        'user': db_user,
        'password': db_password
    }

db_hostname = os.getenv('DB_HOSTNAME')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db_url = f"mysql+pymysql://{credentials['user']}:{credentials['password']}@{db_hostname}:{db_port}/{db_name}?charset=utf8mb4"

engine = create_engine(db_url)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()