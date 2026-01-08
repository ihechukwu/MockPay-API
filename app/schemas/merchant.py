from pydantic import BaseModel, EmailStr


class MerchantCreate(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    password: str


class MerchantLogin(BaseModel):

    email: EmailStr
    password: str
