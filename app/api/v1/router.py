from fastapi import APIRouter
from app.routes.merchant_routes import merchants_router
from app.auth.routes import auths_router
from app.routes.api_keys_routes import api_keys_routers
from app.routes.payments_routes import payments_router

api_router = APIRouter()

api_router.include_router(merchants_router, prefix="/merchants", tags=["Merchants"])
api_router.include_router(auths_router, prefix="/auths", tags=["Authentication"])
api_router.include_router(api_keys_routers, prefix="/api-keys", tags=["API Keys"])
api_router.include_router(payments_router, prefix="/payments", tags=["Payments"])
