from fastapi import status, Depends, APIRouter
# ! APIRouter: Bu FastAPI'dagi routerlar yaratish uchun ishlatiladi. Routerlar yordamida bir guruh yo'laklarni bir joyda jamlash va boshqarish mumkin.
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT 
# ! JWT asosidagi autentifikatsiya uchun ishlatiladi.\

auth_router = APIRouter(
    prefix='/auth'
)

# ? POSTMAN -> HEADERS -> add Authorization, Bearer `token` - beriladi 
# ? ELATMA!!!!!!!! `` - olib tashlanadi tokenni o'zi beriladi
@auth_router.get('/')
# ! Authorize argumenti AuthJWT turidagi obyektni o'z ichiga oladi va Depends() yordamida avtomatik ravishda bog'lanadi. Depends() funksiyasi FastAPI ga bu argument uchun qanday qiymatni olish kerakligini bildiradi.
async def sugnup_main(Authorize: AuthJWT = Depends()):
    try:
        # * Agar token haqiqiy bo'lsa, funksiya davom etadi. Authorize.jwt_required() metodi JWT tokenining mavjudligini va uning yaroqliligini tekshiradi.
        Authorize.jwt_required()
    except Exception as e:
        # ? Agar JWT tekshiruvi muvaffaqiyatsiz bo'lsa yoki istisno yuz bersa, except bloki ishga tushadi va HTTPException chiqariladi. Bu HTTP 401 status kodi va "Invalid Token" detallari bilan javob qaytaradi, bu esa foydalanuvchini autentifikatsiya qilinmaganligini bildiradi.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {'message': 'Bu asosiy auth route'}