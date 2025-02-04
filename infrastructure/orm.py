from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Table, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class CustomerORM(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(column=CustomerORM.id, ondelete="CASCADE"))
    ship_datetime = Column(DateTime, nullable=True)


order_product_associations = Table(
    "order_product_associations",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id", ondelete="CASCADE")),
    Column("product_id", ForeignKey("products.id", ondelete="CASCADE")),
)

OrderORM.products = relationship("ProductORM", secondary=order_product_associations)
