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