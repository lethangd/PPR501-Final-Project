"""Student service with server-side pagination support."""

from __future__ import annotations

import math
from typing import List, Optional

from ..models.student import PaginatedStudents, Student
from ..student_api import StudentApiClient
from ..xml_parser import StudentRecord


class StudentService:
    """Service for student CRUD operations - Direct API access (no cache)."""
    
    def __init__(self, api_client: StudentApiClient):
        self.api = api_client
    
    def get_paginated(
        self, 
        page: int = 0, 
        page_size: int = 15,
        search_query: Optional[str] = None
    ) -> PaginatedStudents:
        """
        Get paginated students with optional search.
        Loads directly from API (no cache).
        """
        # Load all students from API
        all_students = self._load_all_students()
        
        # Filter by search query
        filtered = all_students
        if search_query:
            query_lower = search_query.lower()
            filtered = [
                s for s in all_students
                if (query_lower in s.student_id.lower())
                   or (query_lower in (s.first_name or "").lower())
                   or (query_lower in (s.last_name or "").lower())
                   or (query_lower in (s.email or "").lower())
            ]
        
        # Paginate
        total = len(filtered)
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        start = page * page_size
        end = start + page_size
        page_students = filtered[start:end]
        
        return PaginatedStudents(
            students=page_students,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def get_all_for_stats(self) -> List[Student]:
        """Get all students for statistics."""
        return self._load_all_students()
    
    def create(self, data: dict) -> Student:
        """Create new student."""
        from ..xml_parser import to_api_payload
        
        payload = to_api_payload(data, include_student_id=True)
        self.api.create_student(payload)
        return self._dict_to_student(data)
    
    def update(self, student_id: str, data: dict) -> Student:
        """Update existing student."""
        from ..xml_parser import to_api_payload
        
        payload = to_api_payload(data, include_student_id=False)
        self.api.update_student(student_id, payload)
        data["student_id"] = student_id
        return self._dict_to_student(data)
    
    def delete(self, student_id: str) -> None:
        """Delete student."""
        self.api.delete_student(student_id)
    
    def _load_all_students(self) -> List[Student]:
        """Load all students from API."""
        records: List[StudentRecord] = self.api.list_students()
        return [self._record_to_student(r) for r in records]
    
    @staticmethod
    def _record_to_student(record: StudentRecord) -> Student:
        """Convert StudentRecord to Student model."""
        return Student(
            student_id=record.student_id or "",
            last_name=record.last_name,
            first_name=record.first_name,
            email=record.email,
            birth_date=record.birth_date,
            hometown=record.hometown,
            math_score=record.math_score,
            literature_score=record.literature_score,
            english_score=record.english_score,
        )
    
    @staticmethod
    def _dict_to_student(data: dict) -> Student:
        """Convert dict to Student model."""
        from datetime import date as date_type
        
        birth_date = None
        if data.get("birth_date"):
            try:
                birth_date = date_type.fromisoformat(str(data["birth_date"]))
            except (ValueError, TypeError):
                pass
        
        def to_float(val):
            if val is None or val == "":
                return None
            try:
                return float(val)
            except (ValueError, TypeError):
                return None
        
        return Student(
            student_id=data.get("student_id", ""),
            last_name=data.get("last_name"),
            first_name=data.get("first_name"),
            email=data.get("email"),
            birth_date=birth_date,
            hometown=data.get("hometown"),
            math_score=to_float(data.get("math_score")),
            literature_score=to_float(data.get("literature_score")),
            english_score=to_float(data.get("english_score")),
        )
