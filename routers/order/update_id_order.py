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

@order_router.put('/{id}/update', status_code=status.HTTP_200_OK)
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Enter valid access token")
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()

    order_to_update = db.query(Order).filter(Order.id == id).first()
    if order_to_update.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can not update other user's update!")

    order_to_update.quantity = order.quantity
    order_to_update.product_id = order.product_id
    db.commit()

    custom_response = {
        "success": True,
        "code": 200,
        "message": "Your order successfully updated",
        "data": {
            "id": order.id,
            "quantity": order.quantity,
            "product": order.product_id,
            "order_status": order.order_statuses
        }
    }
    return jsonable_encoder(custom_response)
