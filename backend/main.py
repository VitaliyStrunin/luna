import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.base import Base
from src.database.session import engine, async_session_maker
from src.payments.presentation.api.v1.routes import payment_router
from src.payments.infrastructure.messaging.publisher import OutboxPublisher
from src.payments.infrastructure.messaging.broker import create_broker
from src.payments.infrastructure.messaging.producer import MessageProducer
from src.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    broker = create_broker(settings.rabbitmq_url)
    producer = MessageProducer(broker)
    outbox_publisher = OutboxPublisher(async_session_maker, producer)
    
    publisher_task = asyncio.create_task(outbox_publisher.run())
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    outbox_publisher.stop()
    await publisher_task.cancel()
    await engine.dispose()
    

app = FastAPI(lifespan=lifespan)

app.include_router(payment_router)