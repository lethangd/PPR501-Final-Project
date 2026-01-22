"""
Services module - Business logic layer.

Module này chứa các service classes thực hiện business logic,
tách biệt khỏi API layer để dễ test và maintain.
"""

from app.services.student_service import StudentService

__all__ = ["StudentService"]
