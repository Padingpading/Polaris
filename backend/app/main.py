"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.response import fail
from app.db.base import Base
from app.db.init_data import init_db
from app.db.session import SessionLocal, engine

# Ensure models are registered on metadata.
import app.models  # noqa: F401


def _ensure_database() -> None:
    """Create target MySQL database if it does not exist."""
    db_url = settings.database_url
    if not db_url.startswith("mysql"):
        return

    db_part = db_url.rsplit("/", 1)[-1]
    db_name = db_part.split("?", 1)[0]
    server_url = f"{db_url.rsplit('/', 1)[0]}/mysql"

    bootstrap = create_engine(server_url, pool_pre_ping=True, future=True)
    with bootstrap.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        conn.commit()
    bootstrap.dispose()


@asynccontextmanager
async def lifespan(_: FastAPI):
    _ensure_database()
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        init_db(session)
    yield
    engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(exc.message, code=exc.code, data=exc.details),
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=fail("Validation error", code=42200, data=exc.errors()),
    )


@app.get("/health", tags=["System"])
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "orm": "SQLAlchemy 2.0 + PyMySQL",
    }


app.include_router(api_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
