from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from src.enums import UserRole, OrderStatus, PaymentStatus, PaymentMethod

class UserPostDTO(BaseModel):
    email: str
    password_hash: str

class UserGetDTO(UserPostDTO):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserRelDTO(UserGetDTO):
    profile: "UserProfileGetDTO"
    orders: list["OrderGetDTO"]
    cart_items: list["CartItemGetDTO"]
    reviews: list["ReviewGetDTO"]

class UserProfilePostDTO(BaseModel):
    user_id: int
    username: str

class UserProfileGetDTO(UserProfilePostDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserProfileRelDTO(UserProfileGetDTO):
    user: "UserGetDTO"

class ProductPostDTO(BaseModel):
    title: str
    description: str
    price: float
    sku: str

class ProductGetDTO(ProductPostDTO):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProductRelDTO(ProductGetDTO):
    categories: list["CategoryGetDTO"]
    images: list["ProductImageGetDTO"]
    order_items: list["OrderItemGetDTO"]
    cart_items: list["CartItemGetDTO"]

class CategoryPostDTO(BaseModel):
    id: int
    parent_category_id: Optional[int]

class CategoryGetDTO(CategoryPostDTO):
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryRelDTO(CategoryGetDTO):
    products: list['ProductGetDTO']

class ProductImagePostDTO(BaseModel):
    product_id: int
    image_url: str
    is_main: bool

class ProductImageGetDTO(ProductImagePostDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProductImageRelDTO(ProductImageGetDTO):
    product: "ProductGetDTO"

class OrderPostDTO(BaseModel):
    user_id: int
    status: OrderStatus
    total_amount: float

class OrderGetDTO(OrderPostDTO):
    id: int
    order_date: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderRelDTO(OrderGetDTO):
    user: "UserGetDTO"
    items: list["OrderItemGetDTO"]
    payment: "PaymentGetDTO"

class OrderItemPostDTO(BaseModel):
    order_id: int
    product_id: Optional[int]
    quantity: int
    price_at_purchase: float

class OrderItemGetDTO(OrderItemPostDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemRelDTO(OrderItemGetDTO):
    order: "OrderGetDTO"
    product: "ProductGetDTO"

class CartItemPostDTO(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CartItemGetDTO(CartItemPostDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CartItemRelDTO(CartItemGetDTO):
    user: "UserGetDTO"
    product: "ProductGetDTO"

class PaymentPostDTO(BaseModel):
    order_id: int
    amount: float
    status: PaymentStatus
    payment_method: PaymentMethod
    transaction_id: Optional[str]

class PaymentGetDTO(PaymentPostDTO):
    id:int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaymentRelDTO(PaymentGetDTO):
    order: "OrderGetDTO"

class ReviewGetDTO(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class ReviewPostDTO(ReviewGetDTO):
    id: int
    created_at: datetime

class ReviewRelDTO(ReviewPostDTO):
    user: "UserGetDTO"
    product: "ProductGetDTO"

UserRelDTO.model_rebuild()
ProductRelDTO.model_rebuild()
CategoryRelDTO.model_rebuild()
OrderRelDTO.model_rebuild()
PaymentRelDTO.model_rebuild()
ReviewRelDTO.model_rebuild()