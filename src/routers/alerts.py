from datetime import datetime, timedelta
from functools import cache

from fastapi import APIRouter
from sqlalchemy import select

from src import models, schemas, validations
from src.aliases import DatetimeOrNoneQuery
from src.orm import session_maker
from src.security.auth import AuthenticatedToken

router = APIRouter(prefix="/alerts")


@cache
@router.get("/", status_code=200, tags=["alerts"])
async def list_alerts(
    token: AuthenticatedToken,
    customer_id: str | None = None,
    start_date: DatetimeOrNoneQuery = None,
    end_date: DatetimeOrNoneQuery = None,
) -> list[schemas.Alert]:
    """
    Obtém os alertas das câmeras.

    Filtros:
    - **customer_id**: Apenas alertas relacionados a este cliente.
    - **start_date**: Alertas após esta data e hora (formato UTC).
    - **end_date**: Alertas antes desta data e hora (formato UTC).

    Se **start_date** e **end_date** estiverem vázios, seram pegos alertas do último dia.
    """
    statement = select(models.Alert)

    if customer_id:
        statement = statement.join(models.Camera).where(
            models.Camera.customer_id == customer_id
        )

    if start_date:
        start_date = datetime.combine(start_date.date(), start_date.time())
        statement = statement.where(models.Alert.occurred_at > start_date)
    elif not end_date:
        start_date = datetime.utcnow() - timedelta(days=1)
        statement = statement.where(models.Alert.occurred_at > start_date)

    if end_date:
        end_date = datetime.combine(end_date.date(), end_date.time())
        validations.positive_time_interval(start_date, end_date)
        statement = statement.where(models.Alert.occurred_at < end_date)

    async with session_maker() as session:
        result = await session.execute(statement)
        alerts = result.scalars().all()
        alerts = [schemas.Alert(**a.__dict__) for a in alerts]

    return alerts


@router.post("/", status_code=201, tags=["alerts"])
async def add_alerts(token: AuthenticatedToken, alerts: list[schemas.Alert]):
    """
    Adiciona novos alertas.

    - **id**: Identificador único para o alerta.
    - **occurred_at**: Data e hora que o alerta ocorreu (formato UTC).
    - **camera_id**: Câmera a qual este alerta pertence.
    """
    async with session_maker() as session:
        async with session.begin():
            session.add_all([models.Alert(**alert.model_dump()) for alert in alerts])
