from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Product, Check
from src.schemas.check import CheckRequest


async def create_products(products: list, check_id: int, db: AsyncSession):
    for item in products:
        product_total = item.price * item.quantity
        new_product = Product(
            check_id=check_id,
            name=item.name,
            price=item.price,
            quantity=item.quantity,
            total=product_total
        )
        db.add(new_product)
    await db.commit()


async def create_check(body: CheckRequest, current_user: User, total: float, rest: float,
                       db: AsyncSession = Depends(get_db)):
    """
    The CheckRequest function creates a new check in the database.

    :param rest: Rest amount for user
    :param total: Total payment amount
    :param current_user: Current user from the database
    :param body: CheckRequest: Validate the request body
    :param db: AsyncSession: Get the database session from the dependency
    :return: The newly created check object
    :doc-author: Babenko Vladyslav
    """

    new_check = Check(
        user_id=current_user.id,
        payment_type=body.payment.type,
        payment_amount=body.payment.amount,
        total=total,
        rest=rest
    )
    db.add(new_check)
    await db.commit()
    await db.refresh(new_check)
    print(new_check.id)
    await create_products(products=body.products, check_id=new_check.id, db=db)
    return new_check
