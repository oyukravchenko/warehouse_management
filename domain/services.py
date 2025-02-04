from datetime import datetime
from typing import List

from .models import Customer, Email, Order, Product
from .repositories import (CustomerRepository, OrderRepository,
                           ProductRepository)


class WarehouseService:
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        customer_repo: CustomerRepository,
    ):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.customer_repo = customer_repo

    def create_customer(self, name: str, email: Email, address: str) -> Customer:
        customer = Customer(id=None, name=name, email=email, address=address)
        self.customer_repo.add(customer)
        return customer

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        product = Product(id=None, name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, customer: Customer, products: list[Product]) -> Order:
        order = Order(id=None, customer=customer)
        for p in products:
            order.add_product(p)
        self.order_repo.add(order)
        return order


class ShipmentService:
    def __init__(self, customer_repo: CustomerRepository, order_repo: OrderRepository):
        self.customer_repo = customer_repo
        self.order_repo = order_repo

    def ship_order(self, order: Order):
        order = self.order_repo.get(order.id)

        # some shipping logic here
        ...

        order.ship_datetime = datetime.now()
        self.notify_customer(
            order=order, message="Dear Customer! \n You order has been shipped!"
        )
        self.order_repo.add(order)

    def notify_customer(self, order: Order, message):
        print(f"To: {order.customer.email}\n Order {order.id}\n {message}")
