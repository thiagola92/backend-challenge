from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src import models
from src.orm import session_maker
from src.security.auth import AuthenticatedToken

router = APIRouter(prefix="/camera")


@router.patch("/{id}/disable", status_code=200, tags=["camera"])
async def disable_camera(token: AuthenticatedToken, id: str):
    """
    Desativa uma câmera.
    """
    statement = select(models.Camera).where(models.Camera.id == id)

    async with session_maker() as session:
        result = await session.execute(statement)
        camera = result.scalars().first()

        if not camera:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No camera with this id",
            )

        camera.is_enabled = False
        await session.commit()


@router.patch("/{id}/enable", status_code=200, tags=["camera"])
async def enable_camera(token: AuthenticatedToken, id: str):
    """
    Ativa uma câmera.
    """
    statement = select(models.Camera).where(models.Camera.id == id)

    async with session_maker() as session:
        result = await session.execute(statement)
        camera = result.scalars().first()

        if not camera:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No camera with this id",
            )

        camera.is_enabled = True
        await session.commit()
