from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Sabid107%23@localhost:5433/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#  THIS MUST EXIST
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()