from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Check
from src.repository import check as repositories_check
from src.services.auth import auth_service
from src.schemas.check import CheckRequest, CheckResponse

router = APIRouter(prefix='/check', tags=['check'])


@router.post("/", response_model=CheckResponse, status_code=status.HTTP_201_CREATED)
async def create_check(
        body: CheckRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)) -> CheckResponse:
    """
    The function of creating a receipt for the sale of goods.
    :param body: AsyncSession: Get the database session
    :param db: AsyncSession: Get the database session
    :param current_user: Get the current user from the database
    :return: The new check object
    """
    total = sum([product.price * product.quantity for product in body.products])
    rest = body.payment.amount - total

    if rest < 0:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")
    new_check = await repositories_check.create_check(body, current_user, total, rest, db)
    products_response = [
        {"name": item.name, "price": item.price, "quantity": item.quantity, "total": item.price * item.quantity}
        for item in body.products
    ]
    check_response = CheckResponse(
        id=new_check.id,
        products=products_response,
        payment=body.payment.dict(),
        total=total,
        rest=rest,
        created_at=new_check.created_at
    )

    return check_response
