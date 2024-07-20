from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from data.scehmas import LoginModel
from database.database import get_db
from models.models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash
from fastapi_jwt_auth import AuthJWT # JWT asosidagi autentifikatsiya uchun ishlatiladi.
from fastapi.encoders import jsonable_encoder # Ma'lumotlarni JSON formatiga o'girish uchun ishlatiladi.
from sqlalchemy import or_
import datetime

auth_router = APIRouter(
    prefix='/auth'
)

@auth_router.post('/login', status_code=200)
def login(user: LoginModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # ! Foydalanuvchini username bo'yicha tekshiramiz
    # ! db_user = db.query(User).filter(User.username == user.username).first()
    
    # ! so'rovda email yoki username kiritilganini tekshiramiz
    db_user = db.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()
    # ! Agar foydalanuvchi mavjud bo'lsa va parol to'g'ri bo'lsa
    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(days=3)

        # ! Access va refresh tokenlarni yaratamiz
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)

        token = {
            'access': access_token,
            'refresh': refresh_token
        }
        response = {
            'success': True,
            'code': 201,
            'message': 'User successfully logged in',
            'data': token
        }

        # Javobni JSON formatiga o'giramiz va qaytaramiz
        return jsonable_encoder(response)
    
    # Agar username yoki parol noto'g'ri bo'lsa, HTTP 400 xatolikni tashlaymiz
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
