"""
Provinces API endpoints.

Module này định nghĩa các REST API endpoints cho Province.
Tất cả responses đều trả về JSON (không phải XML như Students).
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.province import ProvinceListResponse, ProvinceResponse
from app.services.province_service import ProvinceService

router = APIRouter()


@router.get(
    "",
    response_model=ProvinceListResponse,
    summary="Lấy danh sách tỉnh thành",
    description="Lấy danh sách tất cả 63 tỉnh thành Việt Nam, hỗ trợ tìm kiếm.",
)
def list_provinces(
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên tỉnh"),
    db: Session = Depends(get_db),
) -> ProvinceListResponse:
    """
    Lấy danh sách tỉnh thành.
    
    - **search** (optional): Tìm kiếm theo tên tỉnh (autocomplete)
    
    Returns:
        JSON với danh sách provinces và total count
    """
    if search:
        provinces = ProvinceService.search_by_name(db, search)
    else:
        provinces = ProvinceService.list_all(db)
    
    # Convert to Pydantic models
    province_responses = [ProvinceResponse.model_validate(p) for p in provinces]
    
    return ProvinceListResponse(
        provinces=province_responses,
        total=len(province_responses)
    )


@router.get(
    "/{province_id}",
    response_model=ProvinceResponse,
    summary="Lấy thông tin một tỉnh thành",
    description="Lấy thông tin chi tiết của một tỉnh thành theo ID.",
)
def get_province(
    province_id: int,
    db: Session = Depends(get_db),
) -> ProvinceResponse:
    """
    Lấy thông tin tỉnh thành theo ID.
    
    - **province_id**: ID của tỉnh thành
    
    Returns:
        JSON với thông tin province
        
    Raises:
        404: Không tìm thấy tỉnh thành
    """
    province = ProvinceService.get_by_id(db, province_id)
    
    if not province:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Không tìm thấy tỉnh thành với ID {province_id}"}
        )
    
    return ProvinceResponse.model_validate(province)
