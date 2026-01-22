"""
Province model.

Module này định nghĩa ORM model cho bảng provinces,
chứa danh sách 63 tỉnh thành Việt Nam.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.student import Student


class Province(Base):
    """
    Model đại diện cho một tỉnh/thành phố.
    
    Attributes:
        id: ID tự tăng (Primary Key)
        code: Mã tỉnh (VD: HN, HCM, DN)
        name: Tên tỉnh/thành phố (VD: Hà Nội, TP. Hồ Chí Minh)
        region: Vùng miền (Bắc, Trung, Nam)
        students: Danh sách sinh viên thuộc tỉnh này
    """
    
    __tablename__ = "provinces"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID tỉnh thành"
    )
    
    # Mã tỉnh (unique)
    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        comment="Mã tỉnh (VD: HN, HCM)"
    )
    
    # Tên tỉnh
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="Tên tỉnh/thành phố"
    )
    
    # Vùng miền
    region: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Vùng miền (Bắc/Trung/Nam)"
    )

    # Relationship với Student (one-to-many)
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="province",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation cho debugging."""
        return f"<Province(id={self.id}, code={self.code}, name={self.name})>"
