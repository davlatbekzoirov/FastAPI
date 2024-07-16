from fastapi import APIRouter

order_router = APIRouter(
    prefix='/order'
)

@order_router.post('/')
async def signup():
    return {'message': 'Sign up'}