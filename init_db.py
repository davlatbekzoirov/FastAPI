from database import engine, Base
from models import User, Order, Product

Base.metadata.create_all(bind=engine)