from fastapi_jwt_auth import AuthJWT # JWT asosidagi autentifikatsiya uchun ishlatiladi.
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

order_router = APIRouter(
    prefix="/order"
)

@order_router.get('/') # ! Bu dekorator routerga yangi yo'lak qo'shadi. Bu yo'lak POST metodi uchun ishlatiladi va URL prefiksi bilan birga /order/ manzilida ishlaydi
async def welcome_page(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    
    return {'message': 'Bu order route sahifasi'}