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
# ? Ma'lumotlar bazasi bilan bog'lanish uchun ishlatiladi.
from sqlalchemy.ext.declarative import declarative_base
# ! ORM (Object Relational Mapping) sinflarini yaratish uchun ishlatiladi
from sqlalchemy.orm import sessionmaker
# ! Ma'lumotlar bazasi sessiyalarini yaratish uchun ishlatiladi

DATABASE_URL = 'postgresql://postgres:d08980476@localhost/delivery_db' 

engine = create_engine(DATABASE_URL)
# ! Ma'lumotlar bazasi bilan bog'lanish uchun create_engine funksiyasini chaqirib, engine obyekti yaratamiz. Bu obyekt SQL aloqalarini amalga oshirish uchun ishlatiladi.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# * sessionmaker yordamida sessiyalarni yaratish uchun konfiguratsiya qilinadi. autocommit=False va autoflush=False parametrlarining qo'llanilishi sessiyaning avtomatik commit va flush (qayd qilish) xatti-harakatlarini o'chiradi. bind=engine esa sessiyani engine ga bog'laydi.
Base = declarative_base()
# ! declarative_base funksiyasini chaqirib Base obyektini yaratamiz. Bu obyekt ORM sinflarini yaratishda asos sifatida ishlatiladi

def get_db():
    db = SessionLocal()
    try:
        # ! Bu generator funktsiya yangi ma'lumotlar bazasi sessiyasini yaratadi va uni foydalanishga beradi (yield db). Funksiya yakunida yoki istisno yuz berganda
        yield db
    finally:    
        db.close()
        # ! db.close() chaqirilib, sessiyani yopadi. Bu funksiya FastAPI yoki boshqa veb-ilovalar uchun dependency injection (bog'lanmalarni qo'shish) sifatida ishlatiladi.
