from src.database import Base
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey, text, Numeric
from enum import Enum
from decimal import Decimal
from datetime import datetime

from typing import Annotated

idpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )]

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'

class OrderStatus(str, Enum):
    PENDING = 'pending'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class PaymentStatus(str, Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'

class PaymentMethod(str, Enum):
    CARD = 'card'
    PAYPAL = 'paypal'

class DiscountType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'

class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[idpk]
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(server_default=UserRole.USER.value)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    profile: Mapped['UserProfileOrm'] = relationship(back_populates='user')
    orders: Mapped[list['OrderOrm']] = relationship(back_populates='user')
    cart_items: Mapped[list['CartItemOrm']] = relationship(back_populates='user')
    reviews: Mapped[list['ReviewOrm']] = relationship(back_populates='user')

class UserProfileOrm(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    username: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(20))
    avatar_url: Mapped[str | None] = mapped_column(String(255))

    user: Mapped['UserOrm'] = relationship(back_populates='profile')


class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int]
    sku: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    categories: Mapped[list['CategoryOrm']] = relationship(
        secondary='product_categories', back_populates='products'
    )
    images: Mapped[list['ProductImageOrm']] = relationship(back_populates='product')
    order_items: Mapped[list['OrderItemOrm']] = relationship(back_populates='product')
    cart_items: Mapped[list['CartItemOrm']] = relationship(back_populates='product')


class CategoryOrm(Base):
    __tablename__ = 'categories'

    id: Mapped[idpk]
    name: Mapped[str] = mapped_column(String(100), unique=True)
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL')
    )

    products: Mapped[list['ProductOrm']] = relationship(
        secondary='product_categories', back_populates='categories'
    )


class ProductImageOrm(Base):
    __tablename__ = 'product_images'

    id: Mapped[idpk]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    image_url: Mapped[str] = mapped_column(String(255))
    is_main: Mapped[bool] = mapped_column(default=False)

    product: Mapped['ProductOrm'] = relationship(back_populates='images')


class OrderOrm(Base):
    __tablename__ = 'orders'

    id: Mapped[idpk]
    user_id: Mapped[int | None] = mapped_column(  # Разрешаем NULL
        ForeignKey('users.id', ondelete='SET NULL')
    )
    status: Mapped[OrderStatus] = mapped_column(server_default=OrderStatus.PENDING.value)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    order_date: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    user: Mapped['UserOrm'] = relationship(back_populates='orders')
    items: Mapped[list['OrderItemOrm']] = relationship(back_populates='order')
    payment: Mapped['PaymentOrm'] = relationship(back_populates='order')


class OrderItemOrm(Base):
    __tablename__ = 'order_items'

    id: Mapped[idpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int | None] = mapped_column(  # Разрешаем NULL
        ForeignKey('products.id', ondelete='SET NULL')
    )
    quantity: Mapped[int]
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped['OrderOrm'] = relationship(back_populates='items')
    product: Mapped['ProductOrm'] = relationship(back_populates='order_items')


class CartItemOrm(Base):
    __tablename__ = 'cart_items'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped['UserOrm'] = relationship(back_populates='cart_items')
    product: Mapped['ProductOrm'] = relationship(back_populates='cart_items')


class PaymentOrm(Base):
    __tablename__ = 'payments'

    id: Mapped[idpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), unique=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[PaymentStatus] = mapped_column(server_default=PaymentStatus.PENDING.value)
    payment_method: Mapped[PaymentMethod]
    transaction_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    created_at: Mapped[created_at]

    order: Mapped['OrderOrm'] = relationship(back_populates='payment')


class ReviewOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[created_at]

    user: Mapped['UserOrm'] = relationship(back_populates='reviews')
    product: Mapped['ProductOrm'] = relationship()

product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
)
