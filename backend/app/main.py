from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.core.redis import redis_client
from app.database import async_session_factory

app = FastAPI(
    title="K8s Production Platform API",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "K8s Production Platform API",
    }


@app.get("/health/live")
async def liveness():
    return {
        "status": "alive",
    }


@app.get("/health/ready")
async def readiness():
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))

        await redis_client.ping()

        return {
            "status": "ready",
            "services": {
                "postgres": "healthy",
                "redis": "healthy",
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Service not ready",
        ) from exc