from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models import Customer, Order, Product
from domain.repositories import (CustomerRepository, OrderRepository,
                                 ProductRepository)

from .orm import CustomerORM, OrderORM, ProductORM


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product):
        product_orm = ProductORM(
            name=product.name, quantity=product.quantity, price=product.price
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id

    def get(self, product_id: int) -> Optional[Product]:
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).one()

        if not product_orm:
            return None

        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
        )

    def list(self) -> List[Product]:
        products_orm = self.session.query(ProductORM).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]


from typing import List, Optional

from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import joinedload


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session, customer_repo: CustomerRepository):
        self.session = session
        self.customer_repo = customer_repo

    def _convert_to_order(self, order_orm: OrderORM) -> Order:
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in order_orm.products
        ]
        customer = self.customer_repo.get(order_orm.customer_id)
        return Order(
            id=order_orm.id,
            customer=customer,
            products=products,
            ship_datetime=order_orm.ship_datetime,
        )

    def add(self, order: Order):
        if order.id:
            order_orm = self.session.query(OrderORM).get(order.id)
            if not order_orm:
                raise ValueError(f"Order with id {order.id} not found")
        else:
            order_orm = OrderORM()

        order_orm.customer_id = order.customer.id
        product_ids = [p.id for p in order.products]
        products = (
            self.session.query(ProductORM).filter(ProductORM.id.in_(product_ids)).all()
        )
        order_orm.products = products
        order_orm.ship_datetime = order.ship_datetime

        if not order.id:
            self.session.add(order_orm)

        self.session.flush()
        order.id = order_orm.id

    def get(self, order_id: int) -> Optional[Order]:
        try:
            order_orm = self.session.query(OrderORM).filter_by(id=order_id).one()
            return self._convert_to_order(order_orm)
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise ValueError(f"Multiple orders found with id {order_id}")

    def list(self) -> List[Order]:
        orders_orm = (
            self.session.query(OrderORM).options(joinedload(OrderORM.products)).all()
        )
        return [self._convert_to_order(order_orm) for order_orm in orders_orm]


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, customer: Customer) -> Customer:
        customer_orm = CustomerORM()
        customer_orm.name = customer.name
        customer_orm.email = customer.email
        customer_orm.address = customer.address
        self.session.add(customer_orm)
        self.session.flush()
        customer.id = customer_orm.id
        return customer

    def get(self, customer_id: int) -> Optional[Customer]:
        customer_orm = self.session.query(CustomerORM).get(customer_id)

        if not customer_orm:
            return None

        return Customer(
            id=customer_orm.id,
            name=customer_orm.name,
            email=customer_orm.email,
            address=customer_orm.address,
        )

    def list(self) -> list[Customer]:
        customers = self.session.query(CustomerORM).all()
        return [Customer(c.id, c.name, c.email, c.address) for c in customers]
