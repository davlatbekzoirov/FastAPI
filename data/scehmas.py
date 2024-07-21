from pydantic import BaseModel
# ! pydantic BaseModel sinfi orqali ma'lumot modellari yaratishga yordam beradi. Bu modellar yordamida kelayotgan yoki jo'natilayotgan ma'lumotlarni tekshirish va validatsiya qilish mumkin.
from typing import Optional
# ? typing kutubxonasi Python kodida tip annotatsiyalarini ishlatish imkonini beradi. Bu kodni yanada tushunarli va o'qiladigan qiladi.
# ? Optional turli tip annotatsiyalarni yaratishda qo'llaniladi va maydonning qiymati None bo'lishi mumkinligini bildiradi.

class SignUPModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]
# * str - majburiy
# * Optional - majburiy emas

    class Config: #  ? Pydantic modeliga maxsus konfiguratsiyalar berish uchun ishlatiladi.
        orm_mode = True
        # ! Bu parametr Pydantic modelining ORM (Object-Relational Mapping) rejimida ishlashiga imkon beradi, ya'ni Pydantic modeli ORM ma'lumotlari bilan ishlash uchun mos bo'ladi.
        schema_extra = {
            'example': {
                'username': 'Davlatbek',
                'email': 'davlatbek@gmail.com',
                'password': 'davlatbek',
                'is_staff': False,
                'is_active': True
            }
        }
        # ! Modelning misolini (example) kiritish imkonini beradi. Bu misol JSON schema yaratishda yordam beradi va hujjatlashtirishda ko'rsatiladi.

class LoginModel(BaseModel):
    username_or_email: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = '431be874dc78c73d440d0706f26fa32b8a37bcd9250930492925c2334cd53a90'
# * import secrets
# * secrets.token_hex()

class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    user: Optional[int]
    product_id: Optional[int]

    class Config: #  ? Pydantic modeliga maxsus konfiguratsiyalar berish uchun ishlatiladi.
        orm_mode = True
        # ! Bu parametr Pydantic modelining ORM (Object-Relational Mapping) rejimida ishlashiga imkon beradi, ya'ni Pydantic modeli ORM ma'lumotlari bilan ishlash uchun mos bo'ladi.
        schema_extra = {
            'example': {
                'quantity': 2
            }
        }
        # ! Modelning misolini (example) kiritish imkonini beradi. Bu misol JSON schema yaratishda yordam beradi va hujjatlashtirishda ko'rsatiladi.

class OrderStatusModel(BaseModel):
    order_statuses: Optional[str] = "PENDING"
    class Config: #  ? Pydantic modeliga maxsus konfiguratsiyalar berish uchun ishlatiladi.
        orm_mode = True
        # ! Bu parametr Pydantic modelining ORM (Object-Relational Mapping) rejimida ishlashiga imkon beradi, ya'ni Pydantic modeli ORM ma'lumotlari bilan ishlash uchun mos bo'ladi.
        schema_extra = {
            'example': {
                'order_statuses': "PENDING"
            }
        }
        # ! Modelning misolini (example) kiritish imkonini beradi. Bu misol JSON schema yaratishda yordam beradi va hujjatlashtirishda ko'rsatiladi.

class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    price: int
    class Config: #  ? Pydantic modeliga maxsus konfiguratsiyalar berish uchun ishlatiladi.
        orm_mode = True
        # ! Bu parametr Pydantic modelining ORM (Object-Relational Mapping) rejimida ishlashiga imkon beradi, ya'ni Pydantic modeli ORM ma'lumotlari bilan ishlash uchun mos bo'ladi.
        schema_extra = {
            'example': {
                'name': "Uzbek Plov",
                'price': 30000
            }
        }
        # ! Modelning misolini (example) kiritish imkonini beradi. Bu misol JSON schema yaratishda yordam beradi va hujjatlashtirishda ko'rsatiladi.
