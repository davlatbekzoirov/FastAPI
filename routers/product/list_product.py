from fastapi_jwt_auth import AuthJWT # ! JWT asosidagi autentifikatsiya uchun ishlatiladi.
from models.models import User, Product
from database.database import get_db
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder # ! Ma'lumotlarni JSON formatiga o'girish uchun ishlatiladi.
from data.scehmas import ProductModel

product_router = APIRouter(
    prefix="/product"
)

@product_router.get('/list', status_code=status.HTTP_201_CREATED)
async def list_all_product(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        products = db.query(Product).all()
        custom_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price 
            }
            for product in products
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only SuperAdmin can see all products")