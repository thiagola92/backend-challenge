from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.config import settings
from src.security.login import UserToken, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_authenticated_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserToken:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm_to_sign_jwt],
        )
    except JWTError:
        raise unauthorized_exception

    try:
        user_token = UserToken(**payload)
    except ValidationError:
        raise unauthorized_exception

    user = await get_user(user_token.username)

    if not user:
        raise unauthorized_exception

    return user_token


AuthenticatedToken = Annotated[UserToken, Depends(get_authenticated_user)]
