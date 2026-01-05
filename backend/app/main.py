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

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.database import engine, get_db
from app.models import Base
from app.services.student_service import StudentService
from app.utils.data_cleaner import data_cleaner


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
    - HTML page cho crawler tại `/students`
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

# Templates cho HTML pages
templates = Jinja2Templates(directory="app/templates")


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


# === HTML Page cho Crawler ===

@app.get(
    "/students",
    response_class=HTMLResponse,
    tags=["Health"],
    summary="HTML table của sinh viên",
    description="Trang HTML hiển thị bảng sinh viên cho mục đích crawling.",
)
def students_html_page(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """
    Render HTML page với bảng sinh viên.
    
    Page này được sử dụng bởi crawler project để scrape data
    bằng pandas.read_html().
    
    Args:
        request: FastAPI Request object
        db: Database session
        
    Returns:
        HTMLResponse với table chứa tất cả sinh viên
    """
    service = StudentService(db)
    students = service.get_all()
    
    records = [service.to_dict(s) for s in students]
    records = data_cleaner.clean_records(records)
    
    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={"students": records},
    )


# === Include API Routers ===

app.include_router(api_router)
