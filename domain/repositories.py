from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Customer, Order, Product


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        pass

    @abstractmethod
    def get(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        pass

    @abstractmethod
    def get(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass


class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer):
        pass

    @abstractmethod
    def get(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def list(self) -> List[Customer]:
        pass
