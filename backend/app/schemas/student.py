"""
Student schemas.

Module này định nghĩa các Pydantic models cho Student entity:
- StudentBase: Fields chung
- StudentCreate: Tạo mới (bao gồm student_id)
- StudentUpdate: Cập nhật (tất cả optional)
- StudentResponse: Response từ API
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    """
    Base schema với các fields chung của Student.
    
    Tất cả các fields đều optional để cho phép:
    - Nhập thông tin không đầy đủ
    - Partial updates
    """
    
    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Họ của sinh viên",
        examples=["Nguyen"]
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Tên của sinh viên",
        examples=["Van A"]
    )
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Địa chỉ email",
        examples=["example@email.com"]
    )
    birth_date: Optional[date] = Field(
        default=None,
        description="Ngày sinh (YYYY-MM-DD)",
        examples=["2000-01-15"]
    )
    hometown: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Quê quán",
        examples=["Ha Noi"]
    )
    math_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Điểm Toán (0-10)",
        examples=[8.5]
    )
    literature_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Điểm Văn (0-10)",
        examples=[7.0]
    )
    english_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Điểm Tiếng Anh (0-10)",
        examples=[9.0]
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Validate email format cơ bản."""
        if v is not None and v.strip():
            v = v.strip()
            if "@" not in v:
                raise ValueError("Email phải chứa ký tự @")
        return v if v else None

    @field_validator("last_name", "first_name", "hometown")
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Loại bỏ whitespace thừa."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None


class StudentCreate(StudentBase):
    """
    Schema cho việc tạo mới sinh viên.
    
    Yêu cầu bắt buộc: student_id
    """
    
    student_id: str = Field(
        min_length=1,
        max_length=20,
        description="Mã số sinh viên (bắt buộc)",
        examples=["SV0001"]
    )

    @field_validator("student_id")
    @classmethod
    def validate_student_id(cls, v: str) -> str:
        """Validate và chuẩn hóa student_id."""
        v = v.strip().upper()
        if not v:
            raise ValueError("Mã sinh viên không được để trống")
        return v


class StudentUpdate(StudentBase):
    """
    Schema cho việc cập nhật sinh viên.
    
    Tất cả fields đều optional - chỉ cập nhật những fields
    được gửi lên trong request.
    """
    pass


class StudentResponse(StudentCreate):
    """
    Schema cho response trả về từ API.
    
    Kế thừa từ StudentCreate, bao gồm tất cả thông tin
    của một sinh viên.
    """
    
    model_config = ConfigDict(
        from_attributes=True,  # Cho phép tạo từ ORM model
        json_schema_extra={
            "example": {
                "student_id": "SV0001",
                "last_name": "Nguyen",
                "first_name": "Van A",
                "email": "vana@example.com",
                "birth_date": "2000-01-15",
                "hometown": "Ha Noi",
                "math_score": 8.5,
                "literature_score": 7.0,
                "english_score": 9.0,
            }
        }
    )
