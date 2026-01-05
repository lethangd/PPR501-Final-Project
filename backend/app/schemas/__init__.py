"""
Schemas module - Pydantic models cho validation và serialization.

Module này chứa các Pydantic schemas để:
- Validate dữ liệu đầu vào từ API requests
- Serialize dữ liệu đầu ra cho API responses
"""

from app.schemas.student import (
    StudentBase,
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)

__all__ = [
    "StudentBase",
    "StudentCreate", 
    "StudentUpdate",
    "StudentResponse",
]
