from fastapi import APIRouter

health_router = APIRouter(prefix="/health")


@health_router.get("/", status_code=200)
async def health():
    return {"status": "ok"}
