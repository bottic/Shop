from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, text, Float

from datetime import datetime
from src.enums import UserRole, OrderStatus, PaymentStatus, PaymentMethod
from typing import Annotated

idpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
)]




class UserTable(Base):
    __tablename__ = 'users'

    id: Mapped[idpk]
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(server_default=UserRole.USER.value)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    profile: Mapped['UserProfileTable'] = relationship(back_populates='user')
    orders: Mapped[list['OrderTable']] = relationship(back_populates='user')
    cart_items: Mapped[list['CartItemTable']] = relationship(back_populates='user')
    reviews: Mapped[list['ReviewOrm']] = relationship(back_populates='user')




class UserProfileTable(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    username: Mapped[str] = mapped_column(String(50))

    user: Mapped['UserTable'] = relationship(back_populates='profile')


class ProductTable(Base):
    __tablename__ = 'products'

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))
    price: Mapped[float] = mapped_column(Float)
    sku: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    categories: Mapped[list['CategoryTable']] = relationship(
        secondary='product_categories', back_populates='products'
    )
    images: Mapped[list['ProductImageTable']] = relationship(back_populates='product')
    order_items: Mapped[list['OrderItemTable']] = relationship(back_populates='product')
    cart_items: Mapped[list['CartItemTable']] = relationship(back_populates='product')


class CategoryTable(Base):
    __tablename__ = 'categories'

    id: Mapped[idpk]
    name: Mapped[str] = mapped_column(String(100), unique=True)
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL')
    )

    products: Mapped[list['ProductTable']] = relationship(
        secondary='product_categories', back_populates='categories'
    )


class ProductImageTable(Base):
    __tablename__ = 'product_images'

    id: Mapped[idpk]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    image_url: Mapped[str] = mapped_column(String(255))
    is_main: Mapped[bool] = mapped_column(default=False)

    product: Mapped['ProductTable'] = relationship(back_populates='images')


class OrderTable(Base):
    __tablename__ = 'orders'

    id: Mapped[idpk]
    user_id: Mapped[int | None] = mapped_column(  # Разрешаем NULL
        ForeignKey('users.id', ondelete='SET NULL')
    )
    status: Mapped[OrderStatus] = mapped_column(server_default=OrderStatus.PENDING.value)
    total_amount: Mapped[float] = mapped_column(Float)
    order_date: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    user: Mapped['UserTable'] = relationship(back_populates='orders')
    items: Mapped[list['OrderItemTable']] = relationship(back_populates='order')
    payment: Mapped['PaymentTable'] = relationship(back_populates='order')


class OrderItemTable(Base):
    __tablename__ = 'order_items'

    id: Mapped[idpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int | None] = mapped_column(  # Разрешаем NULL
        ForeignKey('products.id', ondelete='SET NULL')
    )
    quantity: Mapped[int]
    price_at_purchase: Mapped[float] = mapped_column(Float)

    order: Mapped['OrderTable'] = relationship(back_populates='items')
    product: Mapped['ProductTable'] = relationship(back_populates='order_items')


class CartItemTable(Base):
    __tablename__ = 'cart_items'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped['UserTable'] = relationship(back_populates='cart_items')
    product: Mapped['ProductTable'] = relationship(back_populates='cart_items')


class PaymentTable(Base):
    __tablename__ = 'payments'

    id: Mapped[idpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), unique=True)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[PaymentStatus] = mapped_column(server_default=PaymentStatus.PENDING.value)
    payment_method: Mapped[PaymentMethod]
    transaction_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    created_at: Mapped[created_at]

    order: Mapped['OrderTable'] = relationship(back_populates='payment')


class ReviewOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[created_at]

    user: Mapped['UserTable'] = relationship(back_populates='reviews')
    product: Mapped['ProductTable'] = relationship()

product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
)
