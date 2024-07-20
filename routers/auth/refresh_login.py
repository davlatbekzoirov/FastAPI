from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import User
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT # ? JWT asosidagi autentifikatsiya uchun ishlatiladi.
import datetime


auth_router = APIRouter(
    prefix='/auth'
)  

@auth_router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        access_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(days=3)

        Authorize.jwt_refresh_token_required()  # ? majburiy access token
        current_user = Authorize.get_jwt_subject() # ? access token username-ni ajratib oladi
        
        # ! Database-dan user-ni filter orqali topamiz
        db_user = db.query(User).filter(User.username == current_user).first()

        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
        # ! Access token yaratamiz

        new_access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        
        response = {
            'success': True,
            'code': 200,
            'message': 'New access token is created',
            'data': {
                'access_token': new_access_token
            }
        }
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh Token") from e