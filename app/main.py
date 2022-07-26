from fastapi import FastAPI
from .routers import product, user, auth

app = FastAPI()

app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def route():
    return {"msg": "hello world"}
