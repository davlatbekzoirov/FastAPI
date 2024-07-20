from fastapi import APIRouter

order_router = APIRouter(
    prefix="/order"
)

@order_router.post('/') # ! Bu dekorator routerga yangi yo'lak qo'shadi. Bu yo'lak POST metodi uchun ishlatiladi va URL prefiksi bilan birga /order/ manzilida ishlaydi
async def signup():
    return {'message': 'Sign up'}