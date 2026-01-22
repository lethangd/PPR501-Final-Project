"""
Student Management API.

FastAPI application cho quản lý sinh viên.
Hỗ trợ CRUD operations với API trả về XML.

Author: PPR501 Team
Version: 1.0.0
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.
    
    Chạy khi startup:
    - Tạo tables nếu chưa tồn tại (fallback cho non-docker runs)
    
    Chạy khi shutdown:
    - Cleanup resources nếu cần
    """
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass


# Khởi tạo FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Student Management API
    
    API quản lý sinh viên với các chức năng:
    - **CRUD**: Thêm, sửa, xóa, xem sinh viên
    - **XML Response**: Tất cả endpoints trả về XML
    - **Partial Data**: Cho phép nhập thông tin không đầy đủ
    
    ### Features
    - 100 sinh viên được seed sẵn khi khởi tạo database
    - Hỗ trợ Pandas để tiền xử lý dữ liệu
    """,
    openapi_tags=[
        {
            "name": "Students",
            "description": "CRUD operations cho sinh viên",
        },
        {
            "name": "Health",
            "description": "Health check endpoints",
        },
    ],
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# === Health Check ===

@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Kiểm tra trạng thái hoạt động của API.",
)
def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict với status "ok" nếu service hoạt động
    """
    return {"status": "ok"}


# === Include API Routers ===

app.include_router(api_router)
