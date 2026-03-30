import asyncio
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from src.database.base import Base
from src.database.session import engine
from src.payments.presentation.api.v1.routes import payment_router
from src.payments.infrastructure.messaging.publisher import outbox_publisher
from src.payments.infrastructure.messaging.broker import broker
from src.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    publisher_task = asyncio.create_task(outbox_publisher.run())
    
    yield
    
    outbox_publisher.stop()
    await broker.stop()
    await publisher_task.cancel()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(payment_router)

@app.get("/")
def hello():
    return {"status": "Thank you for checking my test project, I really appreciate that :)"}

@app.get("/health")
def check_health():
    return {"status": "ok"}
 
@app.exception_handler(RequestValidationError)
async def validation_exception_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "Validation error", "errors": exc.errors()}
    )
    