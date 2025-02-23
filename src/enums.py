from enum import Enum

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
