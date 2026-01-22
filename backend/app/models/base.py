"""
Base model cho SQLAlchemy ORM.

Module này định nghĩa DeclarativeBase dùng chung
cho tất cả các models trong ứng dụng.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class cho tất cả SQLAlchemy models.
    
    Tất cả models khác phải kế thừa từ class này
    để được quản lý bởi SQLAlchemy ORM.
    """
    pass
