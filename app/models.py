import datetime
from pydantic import BaseModel, UUID4, EmailStr


class Product(BaseModel):
    id: UUID4
    product_name: str
    category: str
    price: str
    inventory: int
    after_discount: str


class ProductOut(BaseModel):
    products: list[Product]


class ProductIn(BaseModel):
    product_name: str = None
    category: str = None
    price: str = None
    inventory: int = None
    after_discount: str = None


class User(BaseModel):
    username: EmailStr
    password: str
    created_at: datetime.date
    total_transactions: int


class UserReturn(BaseModel):
    id: UUID4
    username: EmailStr
    created_at: datetime.date
    total_transactions: int


class UserOut(BaseModel):
    users: list[UserReturn]


class UserUpdate(BaseModel):
    username: EmailStr = None
    password: str = None
    created_at: datetime.date = None
    total_transactions: int = None
