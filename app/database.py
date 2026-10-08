from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg import OperationalError
from psycopg.rows import dict_row
import time
from .config import settings


SQLALCHEMY_DATABASE_URL=f'postgresql+psycopg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency to get the DB session for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=Djmate",row_factory=dict_row)
#         cursor=conn.cursor()
#         print("database connected sucessfully!")
#         break

#     except OperationalError as e:
#         # Catches connection failures (e.g., wrong password, database offline)
#         print(f"Database connection failed: {e}")
#         time.sleep(2)