from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Формат подключения: postgresql://user:password@localhost:5432/dbname
DATABASE_URL = "postgresql://postgres:gggAAAggg@localhost:6666/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
