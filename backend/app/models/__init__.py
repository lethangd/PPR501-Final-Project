"""
Models module - Định nghĩa các ORM models.

Module này chứa tất cả các SQLAlchemy models tương ứng
với các bảng trong database.
"""

from app.models.base import Base
from app.models.province import Province
from app.models.student import Student

__all__ = ["Base", "Province", "Student"]
