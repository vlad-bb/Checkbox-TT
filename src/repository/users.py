from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function takes an email address and returns the user associated with that email.
    If no user is found, None is returned.

    :param email: str: Pass in the email of the user we want to get from our database
    :param db: AsyncSession: Connect to the database
    :return: A user object if the email exists in the database
    :doc-author: Babenko Vladyslav
    """
    filter_user = select(User).filter_by(email=email)
    user = await db.execute(filter_user)
    user = user.scalar_one_or_none()
    return user


async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    """
    Retrieving user information by their ID from the database.

    :param user_id: int: User ID
    :param db: Session: Database session
    :return: User object from the database
    :doc-author: Babenko Vladyslav
    """
    filter_user = select(User).filter(User.id == user_id)
    user = await db.execute(filter_user)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the request body
    :param db: AsyncSession: Get the database session from the dependency
    :return: The newly created user
    :doc-author: Babenko Vladyslav
    """

    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user's id
    :param token: str | None: Specify that the token parameter can be either a string or none
    :param db: AsyncSession: Pass the database session to the function
    :return: The user
    :doc-author: Babenko Vladyslav
    """
    user.refresh_token = token
    await db.commit()



