# Nothing in this file should be done in production,
# this function only exist to setup for anyone that decide to run the API.
import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import FastAPI
from sqlalchemy import select

from src.config import settings
from src.models import Alert, Camera, Customer
from src.orm import engine, session_maker
from src.security.login import User, password_context


async def wait_db():
    attempts = 0

    while True:
        try:
            async with engine.begin() as conn:
                break
        except:
            attempts += 1

            if attempts > 10:
                raise

            await asyncio.sleep(5)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Customer.metadata.create_all)
        await conn.run_sync(Camera.metadata.create_all)
        await conn.run_sync(Alert.metadata.create_all)


async def exists_free_user() -> bool:
    async with session_maker() as session:
        statement = select(User).where(User.username == settings.api_username)
        result = await session.execute(statement=statement)
        user_found = result.scalars().first()

    return user_found is not None


async def create_free_user():
    async with session_maker() as session:
        async with session.begin():
            session.add(
                User(
                    username=settings.api_username,
                    hashed_password=password_context.hash(settings.api_password),
                )
            )


# Would be best to load from a database backup,
# but i'm trying to make everything happens in one "sudo docker compose up".
# If you know how, please tell me!
async def create_fake_data():
    customer1 = str(uuid4())
    customer2 = str(uuid4())
    customer3 = str(uuid4())
    customer4 = str(uuid4())

    camera1 = str(uuid4())
    camera2 = str(uuid4())
    camera3 = str(uuid4())
    camera4 = str(uuid4())
    camera5 = str(uuid4())
    camera6 = str(uuid4())
    camera7 = str(uuid4())
    camera8 = str(uuid4())

    alert1 = str(uuid4())
    alert2 = str(uuid4())
    alert3 = str(uuid4())
    alert4 = str(uuid4())
    alert5 = str(uuid4())
    alert6 = str(uuid4())

    async with session_maker() as session:
        async with session.begin():
            session.add_all(
                [
                    Customer(id=customer1, name="Alice"),
                    Customer(id=customer2, name="Bob"),
                    Customer(id=customer3, name="Carlos"),
                    Customer(id=customer4, name="Daniel"),
                ]
            )

    async with session_maker() as session:
        async with session.begin():
            session.add_all(
                [
                    Camera(
                        id=camera1,
                        name="cam01",
                        ip="192.168.0.1",
                        is_enabled=True,
                        customer_id=customer1,
                    ),
                    Camera(
                        id=camera2,
                        name="cam02",
                        ip="192.168.0.2",
                        is_enabled=False,
                        customer_id=customer1,
                    ),
                    Camera(
                        id=camera3,
                        name="cam03",
                        ip="192.168.0.3",
                        is_enabled=True,
                        customer_id=customer1,
                    ),
                    Camera(
                        id=camera4,
                        name="cam01",
                        ip="192.168.0.1",
                        is_enabled=True,
                        customer_id=customer2,
                    ),
                    Camera(
                        id=camera5,
                        name="cam02",
                        ip="192.168.0.2",
                        is_enabled=True,
                        customer_id=customer2,
                    ),
                    Camera(
                        id=camera6,
                        name="cam01",
                        ip="127.0.0.1",
                        is_enabled=True,
                        customer_id=customer3,
                    ),
                    Camera(
                        id=camera7,
                        name="cam02",
                        ip="::1",
                        is_enabled=True,
                        customer_id=customer3,
                    ),
                    Camera(
                        id=camera8,
                        name="cam03",
                        ip="0000:0000:0000:0000:0000:0000:0000:0001",
                        is_enabled=True,
                        customer_id=customer3,
                    ),
                ]
            )

    async with session_maker() as session:
        async with session.begin():
            session.add_all(
                [
                    Alert(
                        id=alert1,
                        occurred_at=datetime.utcnow(),
                        camera_id=camera1,
                    ),
                    Alert(
                        id=alert2,
                        occurred_at=datetime.utcnow() - timedelta(hours=1),
                        camera_id=camera1,
                    ),
                    Alert(
                        id=alert3,
                        occurred_at=datetime.utcnow() - timedelta(days=1),
                        camera_id=camera1,
                    ),
                    Alert(
                        id=alert4,
                        occurred_at=datetime.utcnow() - timedelta(days=7),
                        camera_id=camera1,
                    ),
                    Alert(
                        id=alert5,
                        occurred_at=datetime.utcnow() - timedelta(days=3),
                        camera_id=camera4,
                    ),
                    Alert(
                        id=alert6,
                        occurred_at=datetime.utcnow() - timedelta(hours=3),
                        camera_id=camera5,
                    ),
                ]
            )


async def lifespan(app: FastAPI):
    await wait_db()
    await create_tables()

    if not await exists_free_user():
        await create_free_user()
        await create_fake_data()

    yield
