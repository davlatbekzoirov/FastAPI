from fastapi import APIRouter, status
from scehmas import SignUPModel
from database import session, engine
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix='/auth'
)

session = session(bind = engine)

@auth_router.post('/')
async def signup():
    return {'message': 'Sign up'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUPModel):
    db_email = session.query(User).filter(User.email == User.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='User with this email already exists')
    
    db_username = session.query(User).filter(User.username == User.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='User with this username already exists')
    
    new_user = User(
        user = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)
    session.commit()
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