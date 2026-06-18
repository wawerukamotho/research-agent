from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import redis.asyncio as redis

from scaffold.config import settings
from scaffold.logging import setup_logging, logger
from scaffold.observability import setup_observability
from scaffold.errors import AppError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    setup_observability(app)

    # Shared resources
    app.state.db_engine = create_async_engine(settings.database_url)
    app.state.redis = redis.from_url(settings.redis_url)

    logger.info("application_started", environment=settings.environment)
    yield
    # Shutdown
    await app.state.db_engine.dispose()
    await app.state.redis.close()
    logger.info("application_stopped")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/ready")
async def ready_check(request: Request):
    # Check PostgreSQL
    try:
        async with request.app.state.db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("ready_check_failed_postgres", error=str(e))
        raise HTTPException(status_code=503, detail="Database unreachable")

    # Check Redis
    try:
        await request.app.state.redis.ping()
    except Exception as e:
        logger.error("ready_check_failed_redis", error=str(e))
        raise HTTPException(status_code=503, detail="Redis unreachable")

    return {"status": "ready"}


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error(
        "app_error",
        code=exc.code,
        message=exc.message,
        details=exc.details,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception", path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
            }
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
