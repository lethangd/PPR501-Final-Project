"""Province API client for desktop app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import requests


@dataclass(frozen=True)
class Province:
    """Province data model."""
    id: int
    code: str
    name: str
    region: str


class ProvinceApiClient:
    """
    Client để gọi Province API.
    
    Hỗ trợ:
    - Lấy danh sách tất cả tỉnh thành
    - Tìm kiếm tỉnh thành theo tên (autocomplete)
    """
    
    def __init__(self, base_url: str):
        """
        Args:
            base_url: Base URL của API (VD: http://localhost:8000/api)
        """
        self.base_url = base_url.rstrip('/')
        self.provinces_url = f"{self.base_url}/provinces"
    
    def list_all(self) -> List[Province]:
        """
        Lấy danh sách tất cả 63 tỉnh thành.
        
        Returns:
            List[Province]: Danh sách tỉnh thành
            
        Raises:
            requests.RequestException: Nếu request thất bại
        """
        try:
            response = requests.get(self.provinces_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            provinces = data.get('provinces', [])
            
            return [
                Province(
                    id=p['id'],
                    code=p['code'],
                    name=p['name'],
                    region=p['region']
                )
                for p in provinces
            ]
        except requests.RequestException as e:
            print(f"Error fetching provinces: {e}")
            return []
    
    def search(self, query: str) -> List[Province]:
        """
        Tìm kiếm tỉnh thành theo tên (autocomplete).
        
        Args:
            query: Chuỗi tìm kiếm
            
        Returns:
            List[Province]: Danh sách tỉnh thành matching
            
        Raises:
            requests.RequestException: Nếu request thất bại
        """
        try:
            response = requests.get(
                self.provinces_url,
                params={"search": query},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            provinces = data.get('provinces', [])
            
            return [
                Province(
                    id=p['id'],
                    code=p['code'],
                    name=p['name'],
                    region=p['region']
                )
                for p in provinces
            ]
        except requests.RequestException as e:
            print(f"Error searching provinces: {e}")
            return []
    
    def get_by_id(self, province_id: int) -> Province | None:
        """
        Lấy thông tin tỉnh thành theo ID.
        
        Args:
            province_id: ID tỉnh thành
            
        Returns:
            Province | None: Province nếu tìm thấy
        """
        try:
            response = requests.get(
                f"{self.provinces_url}/{province_id}",
                timeout=10
            )
            response.raise_for_status()
            
            p = response.json()
            return Province(
                id=p['id'],
                code=p['code'],
                name=p['name'],
                region=p['region']
            )
        except requests.RequestException:
            return None
