from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.alembic_runner import run_migrations
from app.api.router import master_router
from app.core.exceptions import add_exception_handlers
from app.database import events  # noqa: F401
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(run_migrations)
    yield


app = FastAPI(
    title="Dajavshna",
    docs_url=None,
    redoc_url=None,
    version="0.1.0",
    contact={"Name": "Nika Tsereteli", "email": "ntsereteli19@gmail.com"},
    lifespan=lifespan,
)


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

app.include_router(master_router)


add_exception_handlers(app)


@app.get("/healthcheck", include_in_schema=False)
def get_healthcheck():
    return {"detail": "healthy"}


@app.get("/", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=str(app.openapi_url), title="Dajavshna Api"
    )
