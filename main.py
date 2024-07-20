from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
# ! Bu qatorda fastapi_jwt_auth modulidan AuthJWT import qilinadi. Bu modul JWT (JSON Web Token) yordamida autentifikatsiya qilish uchun ishlatiladi.
from scehmas import LoginModel, Settings

app = FastAPI()

@AuthJWT.load_config
# * Bu dekorator AuthJWT uchun konfiguratsiya yuklash funksiyasini belgilaydi. Bu dekorator yordamida JWT sozlamalari yuklanadi.
def get_config():
    # ? Bu funksiya Settings obyekti qaytaradi, bu JWT sozlamalarini o'z ichiga olgan konfiguratsiya.
    return Settings()


app.include_router(auth_router)
# ! Bu qatorda auth_router FastAPI ilovasiga qo'shiladi. Bu auth_router da belgilangan barcha yo'laklarni ilovaga qo'shadi.
app.include_router(order_router)
# ! Bu qatorda order_router FastAPI ilovasiga qo'shiladi. Bu order_router da belgilangan barcha yo'laklarni ilovaga qo'shadi.

@app.get("/")
async def root():
    return {"message": "Hello World"}