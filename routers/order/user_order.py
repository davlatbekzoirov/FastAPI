from fastapi_jwt_auth import AuthJWT # ! JWT asosidagi autentifikatsiya uchun ishlatiladi.
from models.models import User, Order
from data.scehmas import OrderModel
from database.database import get_db
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder # ! Ma'lumotlarni JSON formatiga o'girish uchun ishlatiladi.


order_router = APIRouter(
    prefix="/order"
)

@order_router.get('/user/orders', status_code=status.HTTP_200_OK) # ! Bu dekorator routerga yangi yo'lak qo'shadi. Bu yo'lak POST metodi uchun ishlatiladi va URL prefiksi bilan birga /order/ manzilida ishlaydi
async def get_user_order(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()

    custom_data = [
        {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statuses.value,
            "total_price": order.quantity * order.product.price
        }
        for order in user.orders
    ]
    return jsonable_encoder(custom_data)