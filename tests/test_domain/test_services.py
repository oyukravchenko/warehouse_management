from datetime import datetime
from unittest.mock import MagicMock

import pytest

from domain.models import Customer, Order, Product
from domain.services import ShipmentService, WarehouseService


@pytest.fixture
def product_repo():
    return MagicMock()


@pytest.fixture
def order_repo():
    return MagicMock()


@pytest.fixture
def customer_repo():
    return MagicMock()


@pytest.fixture
def warehouse_service(product_repo, order_repo, customer_repo):
    return WarehouseService(
        product_repo=product_repo,
        order_repo=order_repo,
        customer_repo=customer_repo,
    )


@pytest.fixture
def shipment_service(customer_repo, order_repo):
    return ShipmentService(
        customer_repo=customer_repo,
        order_repo=order_repo,
    )


def test_create_customer(warehouse_service, customer_repo):
    customer = warehouse_service.create_customer(
        "Ivan Petrov", "ipetrov@example.com", "Moscow, Arbat 1"
    )

    customer_repo.add.assert_called_once()
    assert customer.name == "Ivan Petrov"
    assert customer.email == "ipetrov@example.com"
    assert customer.address == "Moscow, Arbat 1"


def test_create_product(warehouse_service, product_repo):
    product = warehouse_service.create_product("Laptop", 10, 999.99)

    product_repo.add.assert_called_once()
    assert product.name == "Laptop"
    assert product.quantity == 10
    assert product.price == 999.99


def test_create_order_with_products(warehouse_service, order_repo, product_repo):
    customer = Customer(
        id=1, name="Ivan Petrov", email="john@example.com", address="Moscow, Arbat 1"
    )
    product1 = Product(id=1, name="Laptop", quantity=10, price=999.99)
    product2 = Product(id=2, name="Mouse", quantity=50, price=25.99)

    product_repo.get.side_effect = lambda product_id: (
        product1 if product_id == 1 else product2
    )

    order = warehouse_service.create_order(customer, [product1, product2])

    order_repo.add.assert_called_once()
    assert order.customer == customer
    assert order.products == [product1, product2]


def test_ship_order(shipment_service, order_repo):
    customer = Customer(
        id=1, name="Ivan Petrov", email="john@example.com", address="Moscow, Arbat 1"
    )
    order = Order(id=1, customer=customer, ship_datetime=None)

    order_repo.get.return_value = order
    shipment_service.notify_customer = MagicMock()

    shipment_service.ship_order(order)

    order_repo.get.assert_called_once_with(order.id)
    assert order.ship_datetime is not None
    assert isinstance(order.ship_datetime, datetime)
    shipment_service.notify_customer.assert_called_once_with(
        order=order, message="Dear Customer! \n You order has been shipped!"
    )
