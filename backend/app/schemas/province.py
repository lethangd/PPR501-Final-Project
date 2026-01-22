"""
Province schemas.

Module này định nghĩa các Pydantic schemas cho Province,
dùng để validate và serialize dữ liệu API.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProvinceBase(BaseModel):
    """
    Base schema cho Province với các trường cơ bản.
    """
    code: str = Field(..., max_length=10, description="Mã tỉnh (VD: HN, HCM)")
    name: str = Field(..., max_length=100, description="Tên tỉnh/thành phố")
    region: str = Field(..., max_length=20, description="Vùng miền (Bắc/Trung/Nam)")


class ProvinceResponse(ProvinceBase):
    """
    Schema cho response trả về thông tin Province.
    
    Kế thừa tất cả fields từ ProvinceBase và thêm id.
    """
    id: int = Field(..., description="ID tỉnh thành")

    class Config:
        from_attributes = True  # Cho phép tạo từ ORM model


class ProvinceListResponse(BaseModel):
    """
    Schema cho response trả về danh sách provinces.
    """
    provinces: list[ProvinceResponse] = Field(default_factory=list)
    total: int = Field(default=0, description="Tổng số tỉnh thành")
