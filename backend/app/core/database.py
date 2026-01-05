"""
Database connection và session management.

Module này quản lý:
- Engine kết nối PostgreSQL
- Session factory
- Dependency injection cho FastAPI
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# Tạo engine với connection pooling
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
    pool_size=5,         # Số connection trong pool
    max_overflow=10,     # Số connection tối đa khi pool đầy
    echo=settings.debug, # Log SQL queries khi debug
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency để inject database session vào route handlers.
    
    Đảm bảo session được đóng đúng cách sau mỗi request,
    kể cả khi có exception xảy ra.
    
    Yields:
        Session: SQLAlchemy session
        
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
