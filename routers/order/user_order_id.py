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

@order_router.get('/user/order/{id}', status_code=status.HTTP_200_OK)
async def get_user_order_by_id(id: int, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter Valid access token")

    username = Authorize.get_jwt_subject()
    current_user = db.query(User).filter(User.username == username).first()
    order = db.query(Order).filter(Order.id == id, Order.user == current_user).first()

    if order:
        order_data = {
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
            "order_status": order.order_status.value, 
            "total_price": order.quantity * order.product.price
        }
        return jsonable_encoder(order_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order with this ID {id}")
