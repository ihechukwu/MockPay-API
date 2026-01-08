from fastapi import APIRouter
from app.routes.merchant_routes import merchants_router
from app.auth.routes import auths_router

api_router = APIRouter()

api_router.include_router(merchants_router, prefix="/merchants", tags=["Merchants"])
api_router.include_router(auths_router, prefix="/auths", tags=["Authentication"])
