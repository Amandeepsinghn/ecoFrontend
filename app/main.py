from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.order import router as order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(order_router)