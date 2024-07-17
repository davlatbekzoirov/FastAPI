# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# engine = create_engine('postgresql://postgres:d08980476@localhost/delivery_db',
#                        echo=True)

# Base = declarative_base()
# session = sessionmaker()

# def get_db():
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:d08980476@localhost/delivery_db'  # Use your actual database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
