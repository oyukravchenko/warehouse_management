import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


class ValueObject:
    """Base Value Object Class"""


@dataclass
class Email(ValueObject):
    email: str

    def __post_init__(self):
        if not re.match("", self.email):
            raise ValueError(f"Email {self.email} doesn't have valid format")


@dataclass
class Customer:
    id: int
    name: str
    email: Email
    address: str


@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float


@dataclass
class Order:
    id: int
    customer: Customer
    ship_datetime: Optional[datetime] = None
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)
