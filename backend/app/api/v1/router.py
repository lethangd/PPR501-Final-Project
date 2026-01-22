"""
API V1 Router.

Module này tổng hợp tất cả routers của API v1
thành một router chính.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import provinces, students

# Router chính cho API v1
router = APIRouter(prefix="/api")

# Include các sub-routers
router.include_router(
    students.router,
    prefix="/students",
    tags=["Students"],
)

router.include_router(
    provinces.router,
    prefix="/provinces",
    tags=["Provinces"],
)
