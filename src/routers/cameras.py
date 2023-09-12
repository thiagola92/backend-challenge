from functools import cache

from fastapi import APIRouter
from sqlalchemy import select

from src import models, schemas, validations
from src.orm import session_maker
from src.security.auth import AuthenticatedToken

router = APIRouter(prefix="/cameras")


@cache
@router.get("/{customer_id}", status_code=200, tags=["cameras"])
async def list_cameras(
    token: AuthenticatedToken, customer_id: str, enabled: bool = None
) -> list[schemas.Camera]:
    """
    Lista todas as câmeras que pertencem a um determinado cliente.

    Filtros:
    - **customer_id**: Cliente associado às câmeras.
    - **enabled**: Câmeras que estejam ativadas/desativadas.
    """
    statement = select(models.Camera).where(models.Camera.customer_id == customer_id)

    if enabled is not None:
        statement = statement.where(models.Camera.is_enabled == enabled)

    async with session_maker() as session:
        result = await session.execute(statement)
        cameras = result.scalars().all()
        cameras = [schemas.Camera(**c.__dict__) for c in cameras]

    return cameras


@router.post("/", status_code=201, tags=["cameras"])
async def add_cameras(token: AuthenticatedToken, cameras: list[schemas.Camera]):
    """
    Adiciona novas câmeras.

    - **id**: Identificador único para a câmera.
    - **name**: Nome da câmera.
    - **ip**: A qual IP está câmera está associada (único por cliente).
    - **is_enabled**: Se a câmera se encontra ativada/desativada.
    - **customer_id**: O cliente a qual está câmera está associada.
    """
    await validations.all_ips_are_unique_per_customer(cameras)

    async with session_maker() as session:
        async with session.begin():
            session.add_all(
                [models.Camera(**camera.model_dump()) for camera in cameras]
            )
