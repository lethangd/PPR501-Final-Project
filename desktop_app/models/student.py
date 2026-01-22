"""Student data model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Student:
    """Student data model."""
    
    student_id: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None
    hometown: Optional[str] = None
    math_score: Optional[float] = None
    literature_score: Optional[float] = None
    english_score: Optional[float] = None
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        parts = []
        if self.last_name:
            parts.append(self.last_name)
        if self.first_name:
            parts.append(self.first_name)
        return " ".join(parts) if parts else self.student_id
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "student_id": self.student_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "birth_date": str(self.birth_date) if self.birth_date else None,
            "hometown": self.hometown,
            "math_score": self.math_score,
            "literature_score": self.literature_score,
            "english_score": self.english_score,
        }


@dataclass
class PaginatedStudents:
    """Paginated student list with metadata."""
    
    students: list[Student]
    total: int
    page: int
    page_size: int
    total_pages: int
