from fastapi import APIRouter, Depends, BackgroundTasks
from app.services.merchant_service import MerchantService
from app.schemas.merchant import MerchantCreate
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.utils import generate_password_hash
from app.core.email import create_messsage, mail
from app.core.config import settings
from app.auth.utils import create_url_safe_token

merchants_router = APIRouter()
merchant_service = MerchantService()


@merchants_router.post("/register")
async def register(
    merchant_data: MerchantCreate,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    merchant_data.password = generate_password_hash(merchant_data.password)
    merchant = await merchant_service.register(
        merchant_data=merchant_data, session=session
    )

    token = create_url_safe_token({"email": merchant.email})

    link = f"http://{settings.DOMAIN}/api/v1/auths/verify-email?token={token}"

    html = f"""

                <h2>Welcome to the MockPay API services </h2>
                <p>Click <a href= {link} >here </a> to verify account </p>


            """
    subject = "email verification"

    message = create_messsage([merchant.email], subject, html)

    background_task.add_task(mail.send_message, message)

    return {"msg": "account registered, check email for verify account"}
