from fastapi import FastAPI
from routers.auth import auth, login, refresh_login, signup
from routers.order import (order, make_order, list_order, 
                           id_order, user_order, user_order_id, 
                           update_id_order, update_id_status_order,
                           delete_order
)
from routers.product import (create_product, list_product, 
                             id_product, delete_product, update_product
)
from fastapi_jwt_auth import AuthJWT
# ! Bu qatorda fastapi_jwt_auth modulidan AuthJWT import qilinadi. Bu modul JWT (JSON Web Token) yordamida autentifikatsiya qilish uchun ishlatiladi.
from data.scehmas import LoginModel, Settings
from fastapi.middleware.cors import CORSMiddleware
# ! CORS veb-sahifadagi resurslarni manba kelib chiqqan domendan tashqaridagi boshqa domendan qanday qilib so'rash mumkinligini cheklash uchun veb-brauzerlar tomonidan amalga oshiriladigan xavfsizlik xususiyatidir.
import signal
# ! FastAPI dasturini ishga tushirganingizda, ayniqsa ishlab chiqarish muhitida, dasturiy ta'minotning turli xil signal ishlovchilarini boshqarishingiz kerak bo'ladi
import asyncio, uvicorn

app = FastAPI()

@AuthJWT.load_config
# * Bu dekorator AuthJWT uchun konfiguratsiya yuklash funksiyasini belgilaydi. Bu dekorator yordamida JWT sozlamalari yuklanadi.
def get_config():
    # ? Bu funksiya Settings obyekti qaytaradi, bu JWT sozlamalarini o'z ichiga olgan konfiguratsiya.
    return Settings()


app.include_router(auth.auth_router)
app.include_router(login.auth_router)
app.include_router(refresh_login.auth_router)
app.include_router(signup.auth_router)
# ! Bu qatorda auth_router FastAPI ilovasiga qo'shiladi. Bu auth_router da belgilangan barcha yo'laklarni ilovaga qo'shadi.
app.include_router(order.order_router)
app.include_router(make_order.order_router)
app.include_router(list_order.order_router)
app.include_router(id_order.order_router)
app.include_router(user_order.order_router)
app.include_router(user_order_id.order_router)
app.include_router(update_id_order.order_router)
app.include_router(update_id_status_order.order_router)
app.include_router(delete_order.order_router)
# ! Bu qatorda order_router FastAPI ilovasiga qo'shiladi. Bu order_router da belgilangan barcha yo'laklarni ilovaga qo'shadi.
app.include_router(create_product.product_router)
app.include_router(list_product.product_router)
app.include_router(id_product.product_router)
app.include_router(delete_product.product_router)
app.include_router(update_product.product_router)
# ! Bu qatorda order_router FastAPI ilovasiga qo'shiladi. Bu order_router da belgilangan barcha yo'laklarni ilovaga qo'shadi.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ! middleware-larni qo'shamiz

def handle_shutdown_signal(loop, signal):
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
# ! Ushbu funksiya yopish signalini qabul qiladi va event loopdagi barcha vazifalarni bekor qiladi hamda loopni to'xtatadi.

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: handle_shutdown_signal(loop, signame)
        )
    # ! Ushbu kod SIGINT va SIGTERM signallari uchun signal handlerlarni o'rnatadi, bu signallar qabul qilinganda dastur to'g'ri yopilishini ta'minlaydi.

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # ! Nihoyat, dastur uvicorn yordamida ishga tushiriladi
