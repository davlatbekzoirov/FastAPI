from database import engine, Base
# ! engine: Ma'lumotlar bazasi bilan bog'lanish uchun ishlatiladi.
# ! Base: declarative_base orqali yaratilgan va ORM modellar uchun asos bo'lib xizmat qiladi.
from models import User, Order, Product

Base.metadata.create_all(bind=engine)
# ! Bu qatorda Base.metadata.create_all funksiyasi chaqiriladi. Bu funksiya Base obyekti asosida belgilangan barcha jadvallarni ma'lumotlar bazasida yaratadi.
# * Bu parametr engine obyektini create_all funksiyasiga bog'laydi, shunda funksiyani qaysi ma'lumotlar bazasida ishlash kerakligini biladi.