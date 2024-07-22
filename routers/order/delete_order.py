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

@order_router.delete('/{id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def update_order(id: int, Authorize: AuthJWT=Depends(), db: Session = Depends(get_db)):
    """Delete an order of user"""
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Enter valid access token")
    username = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == username).first()

    order = db.query(Order).filter(Order.id == id).first()
    if order.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Kechirasiz, siz boshqa foydalanuvchilarning buyurtmalarini o'chira olmaysiz!")

    if order.order_statuses != "PENDING":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Kechirasiz, siz yolga chiqqan va yetkazib berilgan buyurtmalarni o'chira olmaysiz!")

    db.delete(order)
    db.commit()
    custom_response = {
        "success": True,
        "code": 200,
        "message": "User order is succesfully deleted",
        "data": None
    }
    return jsonable_encoder(custom_response)