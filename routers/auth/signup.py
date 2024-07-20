from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from data.scehmas import SignUPModel
from database.database import get_db
from models.models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash

auth_router = APIRouter(
    prefix='/auth'
)
@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUPModel, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first() # Foydalanuvchini email bo'yicha tekshiramiz
    if db_email is not None:
        # ! Agar email mavjud bo'lsa, HTTP 400 xatolikni tashlaymiz
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User with this email already exists')
    
    # Foydalanuvchini username bo'yicha tekshiramiz
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        # Agar username mavjud bo'lsa, HTTP 400 xatolikni tashlaymiz
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User with this username already exists')
    
    # Yangi foydalanuvchi obyektini yaratamiz
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password), # Parolni hash qilamiz
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    # Yangi foydalanuvchini ma'lumotlar bazasiga qo'shamiz
    db.add(new_user)
    # Ma'lumotlar bazasiga o'zgartirishlarni saqlaymiz
    db.commit()
    # Yangi foydalanuvchini yangilaymiz
    db.refresh(new_user)
    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active
    }
    
    response_model = {
        'success': True,
        'code': 201,
        'message': 'User is created successfully',
        'data': data
    }
    return response_model