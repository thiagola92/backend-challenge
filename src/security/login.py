from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, field_serializer
from sqlalchemy import Column, String, select

from src.config import settings
from src.orm import Base, session_maker

router = APIRouter(prefix="/token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    hashed_password = Column(String)


class UserToken(BaseModel):
    username: str
    expiration_date: datetime

    @field_serializer("expiration_date")
    def serialize_ip(self, expiration_date) -> str:
        return str(expiration_date)


async def get_user(username: str) -> User | None:
    statement = select(User).where(User.username == username).limit(1)

    async with session_maker() as session:
        result = await session.execute(statement)
        return result.scalars().first()


async def get_authenticated_user(username: str, password: str) -> User | None:
    user = await get_user(username)

    if not user:
        return None

    if not password_context.verify(password, user.hashed_password):
        return None

    return user


def create_access_token(username: str) -> str:
    expiration_date = datetime.utcnow() + timedelta(
        settings.access_token_duration_minutes
    )

    user_token = UserToken(
        username=username,
        expiration_date=expiration_date,
    )

    encoded_jwt = jwt.encode(
        claims=user_token.model_dump(),
        key=settings.secret_key,
        algorithm=settings.algorithm_to_sign_jwt,
    )

    return encoded_jwt


@router.post("/", tags=["login"])
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_authenticated_user(form.username, form.password)

    if not user:
        raise unauthorized_exception

    access_token = create_access_token(username=user.username)

    return {"access_token": access_token, "token_type": "bearer"}


# To generate a hashed password: password_context.hash("password")
