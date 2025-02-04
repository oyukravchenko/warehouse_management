from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.orm import Base, CustomerORM, OrderORM, ProductORM


@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()


def test_create_customer(session):
    customer = CustomerORM(
        name="Ivan Petrov", email="ipetrov@example.com", address="Moscow, Arbat 1"
    )
    session.add(customer)
    session.commit()

    retrieved_customer = (
        session.query(CustomerORM).filter_by(name="Ivan Petrov").first()
    )
    assert retrieved_customer is not None
    assert retrieved_customer.email == "ipetrov@example.com"
    assert retrieved_customer.address == "Moscow, Arbat 1"


def test_create_product(session):
    product = ProductORM(name="Laptop", quantity=10, price=999.99)
    session.add(product)
    session.commit()

    retrieved_product = session.query(ProductORM).filter_by(name="Laptop").first()
    assert retrieved_product is not None
    assert retrieved_product.quantity == 10
    assert retrieved_product.price == 999.99


def test_create_order(session):
    customer = CustomerORM(
        name="Ivan Petrov", email="ipetrov@example.com", address="Moscow, Arbat 1"
    )
    session.add(customer)
    session.commit()

    order = OrderORM(
        customer_id=customer.id, ship_datetime=datetime(2025, 1, 23, 10, 0, 0)
    )
    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderORM).filter_by(customer_id=customer.id).first()
    assert retrieved_order is not None
    assert retrieved_order.customer_id == customer.id
    assert retrieved_order.ship_datetime == datetime(2025, 1, 23, 10, 0, 0)


def test_order_product_association(session):
    customer = CustomerORM(
        name="Ivan Petrov", email="ipetrov@example.com", address="Moscow, Arbat 1"
    )
    product = ProductORM(name="Laptop", quantity=10, price=999.99)
    session.add(customer)
    session.add(product)
    session.commit()

    order = OrderORM(
        customer_id=customer.id, ship_datetime=datetime(2025, 1, 23, 10, 0, 0)
    )
    order.products.append(product)
    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderORM).filter_by(customer_id=customer.id).first()
    assert len(retrieved_order.products) == 1
    assert retrieved_order.products[0].name == "Laptop"


def test_delete_customer(session):
    customer = CustomerORM(
        name="Ivan Petrov", email="ipetrov@example.com", address="Moscow, Arbat 1"
    )
    session.add(customer)
    session.commit()

    order = OrderORM(
        customer_id=customer.id, ship_datetime=datetime(2025, 1, 23, 10, 0, 0)
    )
    session.add(order)
    session.commit()

    session.delete(customer)
    session.commit()

    deleted_customer = session.query(CustomerORM).filter_by(name="Ivan Petrov").first()
    assert deleted_customer is None

    deleted_order = session.query(OrderORM).filter_by(customer_id=customer.id).first()
    assert deleted_order is None
