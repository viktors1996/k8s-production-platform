from fastapi import FastAPI

app = FastAPI(
    title="K8s Production Platform API",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "K8s Production Platform API",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "api",
    }