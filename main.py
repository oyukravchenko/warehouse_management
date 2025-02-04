from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from domain.models import Order, Product
from domain.services import ShipmentService, WarehouseService
from infrastructure.database import DATABASE_URL
from infrastructure.orm import Base, OrderORM, ProductORM
from infrastructure.repositories import (SqlAlchemyCustomerRepository,
                                         SqlAlchemyOrderRepository,
                                         SqlAlchemyProductRepository)
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    customer_repo = SqlAlchemyCustomerRepository(session)
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session, customer_repo)

    warehouse_service = WarehouseService(product_repo, order_repo, customer_repo)
    shipment_service = ShipmentService(customer_repo, order_repo)

    uow = SqlAlchemyUnitOfWork(session)
    with uow:
        customer = warehouse_service.create_customer(
            name="Ivan", email="ivan@mymail.ru", address="Moscow"
        )
        new_product = warehouse_service.create_product(
            name="test1", quantity=1, price=100
        )
        print(f"create product: {new_product}")

        new_order: Order = warehouse_service.create_order(
            customer=customer, products=[new_product]
        )

        print(f"create order: {new_order}")

        shipment_service.ship_order(new_order)


if __name__ == "__main__":
    main()
