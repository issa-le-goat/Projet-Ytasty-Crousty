from fastapi import APIRouter, status

health_router = APIRouter()

@health_router.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "ok"}