"""
XML Serializer.

Module này cung cấp các utilities để serialize data sang XML format.
Sử dụng xml.etree.ElementTree (built-in, không cần thư viện ngoài).
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET


class XmlSerializer:
    """
    Utility class để serialize Python objects sang XML.
    
    Hỗ trợ serialize:
    - Single object -> XML element
    - List of objects -> XML với root element
    
    Example:
        serializer = XmlSerializer()
        xml_str = serializer.serialize_student(student_dict)
        xml_str = serializer.serialize_students(list_of_dicts)
    """

    @staticmethod
    def _to_text(value: Any) -> Optional[str]:
        """
        Chuyển đổi giá trị Python sang text cho XML element.
        
        Args:
            value: Giá trị cần chuyển đổi
            
        Returns:
            String representation hoặc None nếu value là None
        """
        if value is None:
            return None
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, float):
            # Format số thập phân, loại bỏ trailing zeros
            return f"{value:.2f}".rstrip('0').rstrip('.')
        return str(value)

    @staticmethod
    def _dict_to_element(data: Dict[str, Any], tag_name: str) -> ET.Element:
        """
        Chuyển đổi dictionary sang XML Element.
        
        Args:
            data: Dictionary cần chuyển đổi
            tag_name: Tên của root element
            
        Returns:
            ET.Element: XML Element
        """
        root = ET.Element(tag_name)
        
        for key, value in data.items():
            child = ET.SubElement(root, key)
            text = XmlSerializer._to_text(value)
            if text is not None:
                child.text = text
                
        return root

    def serialize_student(self, student: Dict[str, Any]) -> str:
        """
        Serialize một sinh viên sang XML string.
        
        Args:
            student: Dictionary chứa thông tin sinh viên
            
        Returns:
            XML string với encoding declaration
            
        Example:
            >>> serializer.serialize_student({"student_id": "SV001", ...})
            '<?xml version="1.0" encoding="utf-8"?>\\n<student>...'
        """
        element = self._dict_to_element(student, "student")
        return ET.tostring(
            element, 
            encoding="utf-8", 
            xml_declaration=True
        ).decode("utf-8")

    def serialize_students(self, students: List[Dict[str, Any]]) -> str:
        """
        Serialize danh sách sinh viên sang XML string.
        
        Args:
            students: List các dictionary sinh viên
            
        Returns:
            XML string với root element <students>
            
        Example:
            >>> serializer.serialize_students([{...}, {...}])
            '<?xml version="1.0" encoding="utf-8"?>\\n<students>...'
        """
        root = ET.Element("students")
        
        for student in students:
            student_element = self._dict_to_element(student, "student")
            root.append(student_element)
            
        return ET.tostring(
            root, 
            encoding="utf-8", 
            xml_declaration=True
        ).decode("utf-8")


# Singleton instance để sử dụng trong toàn app
xml_serializer = XmlSerializer()
