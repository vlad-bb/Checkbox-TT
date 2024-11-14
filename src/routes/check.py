
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.repository import check as repository_check
from src.services.auth import auth_service
from src.schemas.check import CheckRequest, CheckResponse, CheckResponseList
from src.filters.check import CheckFilter
from src.conf.config import config
from src.conf import messages


router = APIRouter(prefix='/check', tags=['check'])



@router.post("/", response_model=CheckResponse, status_code=status.HTTP_201_CREATED)
async def create_check(
        body: CheckRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)) -> CheckResponse:
    """
    The function of creating a receipt for the sale of goods.
    :param body: CheckRequest: The input data
    :param db: AsyncSession: Get the database session
    :param current_user: Get the current user from the database
    :return: The new check object
    """
    total = sum([product.price * product.quantity for product in body.products])
    rest = body.payment.amount - total

    if rest < 0:
        raise HTTPException(status_code=400, detail=messages.PAYMENT_AMOUNT_INVALID)
    check_id, check_created_at, business_name = await repository_check.create_check(body, current_user, total, rest, db)
    await repository_check.create_products(products=body.products, check_id=check_id, db=db)
    products_response = [
        {"name": item.name, "price": item.price, "quantity": item.quantity, "total": item.price * item.quantity}
        for item in body.products
    ]
    check_response = CheckResponse(
        id=check_id,
        products=products_response,
        payment=body.payment.dict(),
        total=total,
        rest=rest,
        created_at=check_created_at,
        business_name=business_name,
        links={
            "link_html": f"{config.DOMAIN}/{check_id}/html",
            "link_txt": f"{config.DOMAIN}/{check_id}/txt",
            "link_qr": f"{config.DOMAIN}/{check_id}/qr-code",
        }

    )
    return check_response


@router.get("/find/{check_id}", response_model=CheckResponse, status_code=status.HTTP_200_OK)
async def read_check(check_id: int, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)) -> CheckResponse:
    """
        The function return a receipt by id.
        :param check_id: Unique check id.
        :param db: AsyncSession: Get the database session
        :param current_user: Get the current user from the database
        :return: The check object
        """
    check = await repository_check.get_check_by_id(check_id, current_user, db)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Check ID: {check_id} not found")
    return check


@router.get("/select", response_model=CheckResponseList)
async def get_checks(
        check_filter: CheckFilter = FilterDepends(CheckFilter, by_alias=True),
        page: int = Query(ge=0, default=0),
        per_page: int = Query(ge=1, le=100, default=10),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
) -> dict[str, int | list[CheckResponse]]:
    """
    The function use filters to return more specific results
    :param check_filter: Filter class
    :param db: AsyncSession: Get the database session
    :param current_user: Get the current user from the database
    :return: List with CheckResponse objects
    """
    checks = await repository_check.get_checks_by_filter(check_filter, current_user, page, per_page, db)
    return checks




