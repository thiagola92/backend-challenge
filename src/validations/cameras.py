from fastapi import HTTPException, status
from sqlalchemy import select

from src import models, schemas
from src.orm import session_maker


async def all_ips_are_unique_per_customer(cameras: list[schemas.Camera]):
    # A set to hold strings like "bob:192.168.0.1", "alice:127.0.0.1", ...
    cusomter_ips = set()

    # Local validation.
    for camera in cameras:
        cusomter_ip = f"{camera.customer_id}:{camera.ip}"

        if cusomter_ip in cusomter_ips:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="IP already used, make sure that IPs are unique per customer",
            )

        cusomter_ips.add(cusomter_ip)

    # Database validation.
    cusomter_ids = [c.customer_id for c in cameras]
    statement = select(models.Camera).where(models.Camera.customer_id.in_(cusomter_ids))

    async with session_maker() as session:
        result = await session.execute(statement)

        for camera in result.scalars().all():
            cusomter_ip = f"{camera.customer_id}:{camera.ip}"

            if cusomter_ip in cusomter_ips:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="IP already used, make sure that IPs are unique per customer",
                )
