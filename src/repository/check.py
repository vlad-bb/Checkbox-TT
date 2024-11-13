import math
from datetime import datetime
from typing import Dict, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.db import get_db
from src.database.models import User, Product, Check
from src.filters.check import CheckFilter
from src.schemas.check import CheckRequest, CheckResponse, ProductResponse, PaymentResponse, CheckResponseList


async def create_products(products: list, check_id: int, db: AsyncSession) -> None:
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
                       db: AsyncSession = Depends(get_db)) -> (int, datetime):
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
    return new_check.id, new_check.created_at


async def get_check_by_id(check_id: int, user: User, db: AsyncSession = Depends(get_db)) -> CheckResponse | None:
    """
    Get a check by ID.

    :param user:  Current user from the database
    :param check_id: int: The unique check ID
    :param db: AsyncSession: The database session
    :return: CheckResponse: The CheckResponse object or None
    """
    filter_check = select(Check).options(
        selectinload(Check.user),
        selectinload(Check.products)
    ).filter_by(id=check_id, user_id=user.id)
    check_expression = await db.execute(filter_check)
    check = check_expression.scalar_one_or_none()
    if check is None:
        return
    return CheckResponse(
        id=check.id,
        products=[
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "total": product.total,
            }
            for product in check.products
        ],
        payment={"type": check.payment_type,
                 "amount": check.payment_amount},
        total=check.total,
        rest=check.rest,
        created_at=check.created_at
    )


async def get_checks_by_filter(check_filter: CheckFilter,
                               user: User, page: int, per_page: int,
                               db: AsyncSession = Depends(get_db)) -> dict[str, int | list[CheckResponse]]:
    """
    Get checks by filters
    :param check_filter: Filter class
    :param user: Current user from the database
    :param db: AsyncSession: The database session
    :return: The list with CheckResponse objects or empty list
    """
    query = select(Check).join(Product).join(User).where(User.id == user.id)
    query = check_filter.filter(query)
    result = await db.execute(query)
    checks = result.scalars().unique().all()
    check_responses = []
    offset_min = page * per_page
    offset_max = (page + 1) * per_page
    for check in checks[offset_min:offset_max]:
        product_responses = [
            ProductResponse(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.total
            )
            for product in check.products
        ]

        payment_response = PaymentResponse(
            type=check.payment_type,
            amount=check.payment_amount
        )

        check_response = CheckResponse(
            id=check.id,
            products=product_responses,
            payment=payment_response,
            total=check.total,
            rest=check.rest,
            created_at=check.created_at
        )

        check_responses.append(check_response)
    return {"entries": check_responses,
            "page": page,
            "per_page": per_page,
            "total": len(checks)
            }
