import qrcode

from io import BytesIO
from fastapi.responses import Response, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Depends, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.db import get_db
from src.repository import check as repository_check
from src.services.check import CheckView

router = APIRouter(tags=['view'])
templates = Jinja2Templates(directory="src/templates")


@router.get("/{check_id}/html", response_class=HTMLResponse)
async def show_check_html(check_id: int,
                          request: Request,
                          db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    """
        The function return a HTML view of check.
        :param request: Request object
        :param check_id: Unique check id.
        :param db: AsyncSession: Get the database session
        :return: The check text HTML
        """
    check = await repository_check.get_check_by_id(check_id=check_id, db=db)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Check ID: {check_id} not found")
    items = [item.dict() for item in check.products]
    payment_method = "Картка" if check.payment.type == 'cashless' else 'Готівка'
    current_time = check.created_at.strftime("%d.%m.%Y об %H:%M:%S")
    return templates.TemplateResponse("receipt.html",
                                      {"request": request, "business_name": check.business_name,
                                       "items": items,
                                       "total": check.total,
                                       "payment_method": payment_method,
                                       "change": check.rest,
                                       "current_time": current_time})


@router.get("/{check_id}/txt", response_class=Response)
async def show_check_txt(check_id: int,
                         line_width: int = Query(ge=28, default=32),
                         db: AsyncSession = Depends(get_db)) -> Response:
    """
        The function return a TXT view of check.
        :param line_width: The width of text
        :param check_id: Unique check id.
        :param db: AsyncSession: Get the database session
        :return: The check text TXT
        """
    check = await repository_check.get_check_by_id(check_id=check_id, db=db)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Check ID: {check_id} not found")
    content = CheckView(business_name=check.business_name, items=check.products,
                        total=check.total, payment_method=check.payment.type, change=check.rest, line_width=line_width)
    text_content = content.generate()
    return Response(content=text_content, media_type="text/plain")


@router.get("/{check_id}/qr-code", response_class=Response)
async def show_check_qr(check_id: int,
                        mode: str = Query(default='html', description="txt or html"),
                        db: AsyncSession = Depends(get_db)) -> Response:
    """
        The function return a QR code view of check.
        :param check_id: Unique check id.
        :param db: AsyncSession: Get the database session
        :return: The check qr code
        """
    check = await repository_check.get_check_by_id(check_id=check_id, db=db)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Check ID: {check_id} not found")
    link = f"{config.DOMAIN}/{check.id}/html" if mode == 'html' else f"{config.DOMAIN}/{check.id}/txt"
    # Generate the QR code image
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/png")
