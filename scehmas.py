from pydantic import BaseModel
from typing import Optional

class SignUPModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]
# str - majburiy
# Optional - majburiy emas

    class Config: #  Pydantic modeliga maxsus konfiguratsiyalar berish uchun ishlatiladi.
        orm_mode = True
        # Bu parametr Pydantic modelining ORM (Object-Relational Mapping) rejimida ishlashiga imkon beradi, ya'ni Pydantic modeli ORM ma'lumotlari bilan ishlash uchun mos bo'ladi.
        schema_extra = {
            'example': {
                'username': 'Davlatbek',
                'email': 'davlatbek@gmail.com',
                'password': 'davlatbek',
                'is_staff': False,
                'is_active': True
            }
        }
        # Modelning misolini (example) kiritish imkonini beradi. Bu misol JSON schema yaratishda yordam beradi va hujjatlashtirishda ko'rsatiladi.
class LoginModel(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = '431be874dc78c73d440d0706f26fa32b8a37bcd9250930492925c2334cd53a90'
# import secrets
# secrets.token_hex()