"""
Student Service.

Module này chứa business logic cho Student entity,
bao gồm các thao tác CRUD và data transformation.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """
    Service class xử lý business logic cho Student.
    
    Tách biệt business logic khỏi API layer để:
    - Dễ dàng unit test
    - Tái sử dụng logic ở nhiều nơi
    - Maintain code dễ hơn
    
    Example:
        service = StudentService(db_session)
        students = service.get_all()
    """

    def __init__(self, db: Session) -> None:
        """
        Khởi tạo service với database session.
        
        Args:
            db: SQLAlchemy Session instance
        """
        self.db = db

    def get_all(self) -> List[Student]:
        """
        Lấy tất cả sinh viên, sắp xếp theo mã số.
        
        Returns:
            List[Student]: Danh sách tất cả sinh viên
        """
        return (
            self.db.query(Student)
            .order_by(Student.student_id.asc())
            .all()
        )

    def get_by_id(self, student_id: str) -> Optional[Student]:
        """
        Tìm sinh viên theo mã số.
        
        Args:
            student_id: Mã số sinh viên cần tìm
            
        Returns:
            Student nếu tìm thấy, None nếu không
        """
        return self.db.get(Student, student_id)

    def create(self, data: StudentCreate) -> Student:
        """
        Tạo sinh viên mới.
        
        Args:
            data: Thông tin sinh viên cần tạo
            
        Returns:
            Student: Sinh viên vừa được tạo
            
        Raises:
            ValueError: Nếu student_id đã tồn tại
        """
        # Kiểm tra trùng mã
        if self.get_by_id(data.student_id):
            raise ValueError(f"Mã sinh viên {data.student_id} đã tồn tại")

        student = Student(**data.model_dump())
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update(self, student_id: str, data: StudentUpdate) -> Optional[Student]:
        """
        Cập nhật thông tin sinh viên.
        
        Chỉ cập nhật những fields được gửi lên (exclude_unset=True).
        
        Args:
            student_id: Mã số sinh viên cần cập nhật
            data: Thông tin cần cập nhật
            
        Returns:
            Student nếu cập nhật thành công, None nếu không tìm thấy
        """
        student = self.get_by_id(student_id)
        if not student:
            return None

        # Chỉ cập nhật những fields có trong request
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(self, student_id: str) -> bool:
        """
        Xóa sinh viên.
        
        Args:
            student_id: Mã số sinh viên cần xóa
            
        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """
        student = self.get_by_id(student_id)
        if not student:
            return False

        self.db.delete(student)
        self.db.commit()
        return True

    @staticmethod
    def to_dict(student: Student) -> Dict[str, Any]:
        """
        Chuyển đổi Student model sang dictionary.
        
        Xử lý các kiểu dữ liệu đặc biệt:
        - Decimal -> float
        - date -> string ISO format
        
        Args:
            student: Student model instance
            
        Returns:
            Dict với dữ liệu đã được chuẩn hóa
        """
        def convert_value(value: Any) -> Any:
            """Helper để convert các kiểu dữ liệu."""
            if isinstance(value, Decimal):
                return float(value)
            if isinstance(value, date):
                return value.isoformat()
            return value

        return {
            "student_id": student.student_id,
            "last_name": student.last_name,
            "first_name": student.first_name,
            "email": student.email,
            "birth_date": convert_value(student.birth_date),
            "province_id": student.province_id,
            "province_name": student.province.name if student.province else None,
            "hometown": student.hometown,
            "math_score": convert_value(student.math_score),
            "literature_score": convert_value(student.literature_score),
            "english_score": convert_value(student.english_score),
        }
