from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DB_URL = f'postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine =create_engine(DB_URL)

SessionLocal= sessionmaker(bind=engine, autoflush=False, autocommit= False)

Base = declarative_base()