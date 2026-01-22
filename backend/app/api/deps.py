"""
API Dependencies.

Module này chứa các dependencies dùng chung cho API routes,
được inject thông qua FastAPI's dependency injection system.

Tất cả dependencies được export từ đây để các endpoints
có thể import tập trung từ một nơi.
"""

from __future__ import annotations

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

# Import get_db từ core.database
from app.core.database import get_db as _get_db


def get_db() -> Generator[Session, None, None]:
    """
    Dependency để inject database session vào route handlers.
    
    Re-export từ core.database để tập trung quản lý dependencies
    tại một điểm duy nhất.
    
    Yields:
        Session: SQLAlchemy session
        
    Example:
        @router.get("/students")
        def list_students(db: Session = Depends(get_db)):
            return db.query(Student).all()
    """
    yield from _get_db()


# Export để các module khác import
__all__ = ["get_db", "Depends"]
