"""
Data Cleaner.

Module này sử dụng Pandas để tiền xử lý và làm sạch dữ liệu
trước khi trả về qua API.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

import pandas as pd


class DataCleaner:
    """
    Utility class để làm sạch và chuẩn hóa dữ liệu.
    
    Sử dụng Pandas để:
    - Normalize NaN/NaT thành None
    - Convert Decimal sang float
    - Đảm bảo consistency của dữ liệu
    
    Example:
        cleaner = DataCleaner()
        cleaned = cleaner.clean_records([row1, row2, ...])
    """

    @staticmethod
    def clean_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Làm sạch danh sách records từ database.
        
        Xử lý:
        - NaN, NaT -> None
        - Decimal -> float
        - Giữ nguyên column order
        
        Args:
            records: List các dictionary từ database
            
        Returns:
            List các dictionary đã được làm sạch
        """
        if not records:
            return []

        # Sử dụng Pandas DataFrame để xử lý batch
        df = pd.DataFrame(records)
        
        # Thay thế NaN/NaT bằng None - sử dụng replace thay vì where
        df = df.fillna(value=pd.NA).replace({pd.NA: None})

        # Convert về list of dicts và xử lý từng giá trị
        cleaned: List[Dict[str, Any]] = []
        for record in df.to_dict(orient="records"):
            clean_record: Dict[str, Any] = {}
            for key, value in record.items():
                # Convert Decimal sang float để JSON/XML serializable
                if isinstance(value, Decimal):
                    clean_record[key] = float(value)
                # Xử lý NaN float (pandas có thể trả về NaN float)
                elif isinstance(value, float) and pd.isna(value):
                    clean_record[key] = None
                # Giữ nguyên các giá trị khác
                else:
                    clean_record[key] = value
            cleaned.append(clean_record)

        return cleaned

    @staticmethod
    def clean_single(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Làm sạch một record đơn lẻ.
        
        Wrapper để clean một record thay vì list.
        
        Args:
            record: Dictionary cần làm sạch
            
        Returns:
            Dictionary đã được làm sạch
        """
        result = DataCleaner.clean_records([record])
        return result[0] if result else {}


# Singleton instance
data_cleaner = DataCleaner()
