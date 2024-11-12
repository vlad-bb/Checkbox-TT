from datetime import  datetime
from sqlalchemy import  String, DateTime, Integer, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    checks: Mapped[list["Check"]] = relationship("Check", back_populates="user")


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    payment_type: Mapped[str] = mapped_column(String(10), nullable=False)
    payment_amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    rest: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    user: Mapped[User] = relationship("User", back_populates="checks")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="check", lazy="selectin")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    check: Mapped[Check] = relationship("Check", back_populates="products", lazy="selectin")
