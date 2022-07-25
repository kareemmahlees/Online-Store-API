from pydantic import BaseModel, UUID4


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
