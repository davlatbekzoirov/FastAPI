from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
# * Column - Ma'lumotlar bazasi jadvallarida ustunlar yaratish uchun ishlatiladi. Har bir ustun jadvaldagi ma'lumotlarning turini va xususiyatlarini belgilaydi.
# * Integer - Column obyektlari uchun integer (butun son) tipini belgilaydi
# * Boolean - Column obyektlari uchun boolean (mantiqiy) tipini belgilaydi.
# * Text - Column obyektlari uchun uzun matn saqlash uchun ishlatiladi.
# * String - Column obyektlari uchun qisqa matn saqlash uchun ishlatiladi.
# * ForeignKey - Tashqi kalitlar yaratish uchun ishlatiladi. Bu boshqa jadvaldagi ustunga bog'langan ustunlarni belgilaydi.
from sqlalchemy.orm import relationship
# * relationship - SQLAlchemy'da jadvaldagi qatorlar o'rtasida bog'lanishlarni belgilash uchun ishlatiladi. Bu bog'lanishlar one-to-many, many-to-one, one-to-one, va many-to-many turlarida bo'lishi mumkin.
from sqlalchemy_utils.types import ChoiceType
# * ChoiceType - ChoiceType ma'lumot turini belgilash uchun ishlatiladi, bu ustun uchun faqat belgilangan qiymatlar to'plamini qabul qiladi. Bu, asosan, oldindan belgilangan variantlar to'plamiga ega ustunlar uchun ishlatiladi.

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(25), unique = True)
    email = Column(String(70), unique = True)
    password = Column(Text, nullable = True)
    is_staff = Column(Boolean, default = False)
    is_active = Column(Boolean, default = False)
    orders = relationship('Order', back_populates = 'user') # ? ONE-TO-MANY RELATIONSHIP
    # ! User va Order jadvallari o'rtasida "bitta userning ko'p orderlari bo'lishi mumkin" munosabati (ONE-TO-MANY).
    
    def __repr__(self):
        return f"<user {self.username}" # ! Chiroyliroq qilishi uchun ishlatiladi
    
class Order(Base):
    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )
    __tablename__ = 'orders'
    id = Column(Integer, primary_key = True)
    quantity = Column(Integer, nullable=False)
    ordered_statuses = Column(ChoiceType(ORDER_STATUSES),
                              default = 'PENDING')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates = 'orders') # ? MANY-TO-ONE RELATIONSHIP
    # ! Order va User jadvallari o'rtasida "ko'p orderlar bitta userga tegishli bo'lishi mumkin" munosabati (MANY-TO-ONE).
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates = 'orders')
    # ! Order va Product jadvallari o'rtasida munosabat.

    def __repr__(self):
        return f"<order {self.id}" # ! Chiroyliroq qilishi uchun ishlatiladi
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    name = Column(String(100))
    price = Column(Integer)
    orders = relationship('Order', back_populates = 'product') # ? ONE-TO-MANY RELATIONSHIP
    
    def __repr__(self):
        return f"<product {self.name}" # ! Chiroyliroq qilishi uchun ishlatiladi