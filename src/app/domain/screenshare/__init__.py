from fastapi import APIRouter

from .router import screenshare_controller

router = APIRouter()
router.include_router(screenshare_controller.router, prefix="/ws", tags=["screen-share"])
