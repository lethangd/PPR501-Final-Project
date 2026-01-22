"""
Province Service.

Business logic layer cho Province operations.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.province import Province


class ProvinceService:
    """
    Service class xử lý business logic cho Province.
    """

    @staticmethod
    def list_all(db: Session) -> List[Province]:
        """
        Lấy danh sách tất cả các tỉnh thành.
        
        Args:
            db: Database session
            
        Returns:
            List[Province]: Danh sách tất cả tỉnh thành (63 tỉnh)
        """
        return db.query(Province).order_by(Province.name).all()
    
    @staticmethod
    def get_by_id(db: Session, province_id: int) -> Optional[Province]:
        """
        Lấy thông tin tỉnh thành theo ID.
        
        Args:
            db: Database session
            province_id: ID tỉnh thành
            
        Returns:
            Optional[Province]: Province nếu tìm thấy, None nếu không
        """
        return db.query(Province).filter(Province.id == province_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Province]:
        """
        Lấy thông tin tỉnh thành theo tên.
        
        Args:
            db: Database session
            name: Tên tỉnh thành
            
        Returns:
            Optional[Province]: Province nếu tìm thấy, None nếu không
        """
        return db.query(Province).filter(Province.name == name).first()
    
    @staticmethod
    def search_by_name(db: Session, query: str) -> List[Province]:
        """
        Tìm kiếm tỉnh thành theo tên (autocomplete).
        
        Args:
            db: Database session
            query: Chuỗi tìm kiếm
            
        Returns:
            List[Province]: Danh sách tỉnh thành matching
        """
        if not query:
            return ProvinceService.list_all(db)
        
        # Search using ILIKE (case-insensitive)
        search_pattern = f"%{query}%"
        return (
            db.query(Province)
            .filter(Province.name.ilike(search_pattern))
            .order_by(Province.name)
            .all()
        )
