"""
Cấu hình ứng dụng.

Module này quản lý tất cả các cấu hình của ứng dụng thông qua
biến môi trường, sử dụng Pydantic Settings để validation.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Cấu hình ứng dụng từ biến môi trường.
    
    Attributes:
        app_name: Tên ứng dụng
        app_version: Phiên bản ứng dụng
        debug: Chế độ debug
        database_url: URL kết nối PostgreSQL
    """
    
    app_name: str = Field(default="Student Management API", description="Tên ứng dụng")
    app_version: str = Field(default="1.0.0", description="Phiên bản")
    debug: bool = Field(default=False, description="Chế độ debug")
    
    # Database
    database_url: str = Field(
        default="postgresql+psycopg2://students_user:students_pass@localhost:5432/students_db",
        description="PostgreSQL connection URL"
    )
    
    # CORS (nếu cần mở rộng sau này)
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Lấy instance Settings (cached).
    
    Sử dụng lru_cache để đảm bảo chỉ tạo 1 instance duy nhất
    trong suốt vòng đời ứng dụng.
    
    Returns:
        Settings: Instance cấu hình ứng dụng
    """
    return Settings()


# Shortcut để truy cập settings
settings = get_settings()
