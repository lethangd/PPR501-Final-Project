"""
Student model.

Module này định nghĩa ORM model cho bảng students,
bao gồm thông tin cá nhân và điểm số của sinh viên.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.province import Province


class Student(Base):
    """
    Model đại diện cho một sinh viên trong hệ thống.
    
    Attributes:
        student_id: Mã số sinh viên (Primary Key)
        last_name: Họ
        first_name: Tên
        email: Địa chỉ email
        birth_date: Ngày sinh
        province_id: ID tỉnh/thành phố (Foreign Key)
        hometown: Quê quán (deprecated, sử dụng province_id)
        math_score: Điểm Toán (0-10)
        literature_score: Điểm Văn (0-10)
        english_score: Điểm Tiếng Anh (0-10)
        
    Note:
        Tất cả các trường ngoại trừ student_id đều có thể NULL,
        cho phép nhập thông tin không đầy đủ.
    """
    
    __tablename__ = "students"

    # Primary key - Mã sinh viên (bắt buộc)
    student_id: Mapped[str] = mapped_column(
        String(20), 
        primary_key=True,
        comment="Mã số sinh viên"
    )

    # Thông tin cá nhân (tất cả optional)
    last_name: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="Họ"
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="Tên"
    )
    email: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="Email"
    )
    birth_date: Mapped[Optional[date]] = mapped_column(
        Date, 
        nullable=True,
        comment="Ngày sinh"
    )
    
    # Province - Foreign Key
    province_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("provinces.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID tỉnh/thành phố"
    )
    
    # Deprecated: Keep for backward compatibility, will be removed
    hometown: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="Quê quán (deprecated)"
    )

    # Relationship với Province
    province: Mapped[Optional["Province"]] = relationship(
        "Province",
        back_populates="students"
    )

    # Điểm số (0-10, optional)
    math_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 2), 
        nullable=True,
        comment="Điểm Toán"
    )
    literature_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 2), 
        nullable=True,
        comment="Điểm Văn"
    )
    english_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 2), 
        nullable=True,
        comment="Điểm Tiếng Anh"
    )

    def __repr__(self) -> str:
        """String representation cho debugging."""
        return f"<Student(id={self.student_id}, name={self.first_name} {self.last_name})>"
