from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from scehmas import SignUPModel, LoginModel
from database import get_db
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT # JWT asosidagi autentifikatsiya uchun ishlatiladi.
from fastapi.encoders import jsonable_encoder # Ma'lumotlarni JSON formatiga o'girish uchun ishlatiladi.
from sqlalchemy import or_


auth_router = APIRouter(
    prefix='/auth'
)

# POSTMAN -> HEADERS -> add Authorization, Bearer `token` - beriladi 
# ELATMA!!!!!!!! `` - olib tashlanadi tokenni o'zi beriladi
@auth_router.get('/')
async def sugnu_main(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {'message': 'Bu asosiy auth route'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUPModel, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first() # Foydalanuvchini email bo'yicha tekshiramiz
    if db_email is not None:
        # Agar email mavjud bo'lsa, HTTP 400 xatolikni tashlaymiz
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


@auth_router.post('/login', status_code=200)
def login(user: LoginModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Foydalanuvchini username bo'yicha tekshiramiz
    # db_user = db.query(User).filter(User.username == user.username).first()
    
    # so'rovda email yoki username kiritilganini tekshiramiz
    db_user = db.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()
    # Agar foydalanuvchi mavjud bo'lsa va parol to'g'ri bo'lsa
    if db_user and check_password_hash(db_user.password, user.password):
        # Access va refresh tokenlarni yaratamiz
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

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