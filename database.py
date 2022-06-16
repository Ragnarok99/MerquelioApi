import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

os.getenv('DB_URL')

SQL_ALCHEMY_DATABASE = os.getenv('DB_URL')

engine = create_engine(SQL_ALCHEMY_DATABASE, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
