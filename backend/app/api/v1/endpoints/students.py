"""
Students API Endpoints.

Module này định nghĩa tất cả REST API endpoints cho Student resource.
Tất cả endpoints trả về XML response theo yêu cầu.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.student_service import StudentService
from app.utils.data_cleaner import data_cleaner
from app.utils.xml_serializer import xml_serializer

# Router cho students endpoints
router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> StudentService:
    """Helper dependency để tạo StudentService instance."""
    return StudentService(db)


@router.get(
    "",
    response_class=Response,
    summary="Lấy danh sách tất cả sinh viên",
    description="Trả về danh sách tất cả sinh viên trong database dưới dạng XML.",
)
def list_students(service: StudentService = Depends(get_service)) -> Response:
    """
    Lấy danh sách tất cả sinh viên.
    
    Returns:
        Response: XML chứa danh sách sinh viên
        
    Example Response:
        ```xml
        <?xml version="1.0" encoding="utf-8"?>
        <students>
            <student>
                <student_id>SV0001</student_id>
                <last_name>Nguyen</last_name>
                ...
            </student>
        </students>
        ```
    """
    students = service.get_all()
    
    # Convert models sang dicts và clean data
    records = [service.to_dict(s) for s in students]
    records = data_cleaner.clean_records(records)
    
    # Serialize sang XML
    xml_content = xml_serializer.serialize_students(records)
    
    return Response(
        content=xml_content,
        media_type="application/xml",
    )


@router.get(
    "/{student_id}",
    response_class=Response,
    summary="Lấy thông tin một sinh viên",
    description="Trả về thông tin chi tiết của một sinh viên theo mã số.",
)
def get_student(
    student_id: str,
    service: StudentService = Depends(get_service),
) -> Response:
    """
    Lấy thông tin một sinh viên theo mã số.
    
    Args:
        student_id: Mã số sinh viên cần tìm
        
    Returns:
        Response: XML chứa thông tin sinh viên
        
    Raises:
        HTTPException 404: Nếu không tìm thấy sinh viên
    """
    student = service.get_by_id(student_id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sinh viên với mã {student_id}",
        )
    
    record = data_cleaner.clean_single(service.to_dict(student))
    xml_content = xml_serializer.serialize_student(record)
    
    return Response(
        content=xml_content,
        media_type="application/xml",
    )


@router.post(
    "",
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo sinh viên mới",
    description="Tạo một sinh viên mới trong database. Chỉ student_id là bắt buộc.",
)
def create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_service),
) -> Response:
    """
    Tạo sinh viên mới.
    
    Args:
        payload: Thông tin sinh viên cần tạo (JSON)
        
    Returns:
        Response: XML chứa thông tin sinh viên vừa tạo
        
    Raises:
        HTTPException 409: Nếu mã sinh viên đã tồn tại
    """
    try:
        student = service.create(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    
    record = data_cleaner.clean_single(service.to_dict(student))
    xml_content = xml_serializer.serialize_student(record)
    
    return Response(
        content=xml_content,
        media_type="application/xml",
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    "/{student_id}",
    response_class=Response,
    summary="Cập nhật thông tin sinh viên",
    description="Cập nhật thông tin sinh viên. Chỉ cập nhật các trường được gửi lên.",
)
def update_student(
    student_id: str,
    payload: StudentUpdate,
    service: StudentService = Depends(get_service),
) -> Response:
    """
    Cập nhật thông tin sinh viên.
    
    Args:
        student_id: Mã số sinh viên cần cập nhật
        payload: Thông tin cần cập nhật (JSON, partial update)
        
    Returns:
        Response: XML chứa thông tin sinh viên sau cập nhật
        
    Raises:
        HTTPException 404: Nếu không tìm thấy sinh viên
    """
    student = service.update(student_id, payload)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sinh viên với mã {student_id}",
        )
    
    record = data_cleaner.clean_single(service.to_dict(student))
    xml_content = xml_serializer.serialize_student(record)
    
    return Response(
        content=xml_content,
        media_type="application/xml",
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa sinh viên",
    description="Xóa một sinh viên khỏi database.",
)
def delete_student(
    student_id: str,
    service: StudentService = Depends(get_service),
) -> Response:
    """
    Xóa sinh viên.
    
    Args:
        student_id: Mã số sinh viên cần xóa
        
    Returns:
        Response: 204 No Content nếu thành công
        
    Raises:
        HTTPException 404: Nếu không tìm thấy sinh viên
    """
    success = service.delete(student_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sinh viên với mã {student_id}",
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
