from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repositories_users

from src.schemas.user import UserSchema, UserResponse, TokenSchema, UserBase
from src.services.auth import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])



@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes in a UserSchema object, which is validated by pydantic.
        If the email already exists, it returns an HTTP 409 Conflict error.
        Otherwise, it hashes the password and adds a new user to the database.

    :param body: UserSchema: Validate the request body
    :param db: AsyncSession: Get the database session
    :return: The new user
    :doc-author: Babenko Vladyslav
    """
    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists!")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)

    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(body: UserBase, db: AsyncSession = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes in the email and password of the user, and returns an access token if successful.
        The access token can be used to make requests on behalf of that user.

    :param body: Get the email and password from the request body
    :param db: AsyncSession: Get the database connection
    :return: A dictionary with the following keys:
    :doc-author: Babenko Vladyslav
    """
    user = await repositories_users.get_user_by_email(body.email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid registration information!")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect registration information!")

    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(auth_service.bearer_schema),
                        db: AsyncSession = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
        It takes in a refresh token and returns an access_token, a new refresh_token, and the type of token.

    :param credentials: HTTPAuthorizationCredentials: Get the token from the header
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the access_token, refresh_token and token type
    :doc-author: Babenko Vladyslav
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token!")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
