from fastapi import APIRouter
# * APIRouter: Bu FastAPI'dagi routerlar yaratish uchun ishlatiladi. Routerlar yordamida bir guruh yo'laklarni bir joyda jamlash va boshqarish mumkin.

order_router = APIRouter( # ! Bu yangi APIRouter obyektini yaratadi.
    prefix='/order' # ! Bu parametr routerdagi barcha yo'laklar uchun URL prefiksini belgilaydi. Bu routerga tegishli barcha yo'laklar URL prefiksiga /order qo'shiladi.
)

@order_router.post('/') # ! Bu dekorator routerga yangi yo'lak qo'shadi. Bu yo'lak POST metodi uchun ishlatiladi va URL prefiksi bilan birga /order/ manzilida ishlaydi
async def signup():
    return {'message': 'Sign up'}