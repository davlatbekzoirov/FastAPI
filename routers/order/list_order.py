from fastapi_jwt_auth import AuthJWT # JWT asosidagi autentifikatsiya uchun ishlatiladi.
from models.models import User, Order
from database.database import get_db
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder # ! Ma'lumotlarni JSON formatiga o'girish uchun ishlatiladi.


order_router = APIRouter(
    prefix="/order"
)

@order_router.get('/list', status_code=status.HTTP_200_OK)
async def list_all_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # ! Bu barcha buyurtmalar ro'yxatini qaytaradi
    try:
        Authorize.jwt_required()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    
    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = db.query(Order).all()
        custom_data = [
            {
                'id': order.id,
                'user_id': {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email
                },
                'product_id': {
                    'id': order.product.id,
                    'name': order.product.name,
                    'price': order.product.price
                },
                'quantity': order.quantity,
                'order_status': order.ordered_statuses.value,
                'total_price': order.quantity * order.product.price
            }
            for order in orders
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only SuperAdmin can see all products")