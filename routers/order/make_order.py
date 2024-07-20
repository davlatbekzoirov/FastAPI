from fastapi_jwt_auth import AuthJWT # JWT asosidagi autentifikatsiya uchun ishlatiladi.
from models.models import User, Order
from data.scehmas import OrderModel
from database.database import get_db
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session


order_router = APIRouter(
    prefix="/order"
)

@order_router.post('/make', status_code=status.HTTP_201_CREATED) # ! Bu dekorator routerga yangi yo'lak qo'shadi. Bu yo'lak POST metodi uchun ishlatiladi va URL prefiksi bilan birga /order/ manzilida ishlaydi
async def make_order(order: OrderModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity = order.quantity,
    )

    new_order.user = user
    db.add(new_order)
    db.commit()

    data = {
        'success': True,
        'code': 201,
        'message':'Order is created successfully',
        'data': {
            'id': new_order.id,
            'quantity': new_order.quantity,
            'order_status': new_order.ordered_statuses,
        }
    }
    return data
