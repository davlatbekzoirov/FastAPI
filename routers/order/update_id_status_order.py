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

@order_router.patch('/{id}/update-status', status_code=status.HTTP_200_OK)
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Enter valid access token")
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()
    if user.is_staff:
        order_to_update = db.query(Order).filter(Order.id == id).first()
        print('order_to_update', order_to_update)
        order_to_update.order_statuses = order.order_statuses
        db.commit()
        print('order updated')

        custom_response = {
            "success": True,
            "code": 200,
            "message": "User order is succesfully updated",
            "data": {
                "id": order_to_update.id,
                "order_status": order_to_update.order_statuses
            }
        }
        return jsonable_encoder(custom_response)