"""XML parsing utilities for the desktop client."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class StudentRecord:
    """In-memory representation used by the Tkinter UI."""

    student_id: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None  # keep as ISO string for the UI
    hometown: Optional[str] = None
    math_score: Optional[str] = None
    literature_score: Optional[str] = None
    english_score: Optional[str] = None

    @staticmethod
    def columns() -> List[str]:
        return [
            "student_id",
            "last_name",
            "first_name",
            "email",
            "birth_date",
            "hometown",
            "math_score",
            "literature_score",
            "english_score",
        ]

    def to_row(self) -> List[str]:
        """Return values in a stable column order (for Treeview insertion)."""
        return [getattr(self, key) or "" for key in self.columns()]


def _text_or_none(el: Optional[ET.Element]) -> Optional[str]:
    if el is None:
        return None
    if el.text is None:
        return None
    value = el.text.strip()
    return value or None


def parse_student_element(student_el: ET.Element) -> StudentRecord:
    """Parse a single <student> element into StudentRecord."""

    def get(tag: str) -> Optional[str]:
        return _text_or_none(student_el.find(tag))

    student_id = get("student_id")
    if not student_id:
        raise ValueError("Invalid XML: missing <student_id>")

    return StudentRecord(
        student_id=student_id,
        last_name=get("last_name"),
        first_name=get("first_name"),
        email=get("email"),
        birth_date=get("birth_date"),
        hometown=get("hometown"),
        math_score=get("math_score"),
        literature_score=get("literature_score"),
        english_score=get("english_score"),
    )


def parse_students_xml(xml_text: str) -> List[StudentRecord]:
    """Parse XML response into a list of StudentRecord."""

    root = ET.fromstring(xml_text)

    if root.tag == "student":
        return [parse_student_element(root)]

    if root.tag != "students":
        raise ValueError(f"Unexpected XML root <{root.tag}> (expected <students> or <student>)")

    records: List[StudentRecord] = []
    for child in root.findall("student"):
        records.append(parse_student_element(child))
    return records


def to_api_payload(values: Dict[str, str], *, include_student_id: bool) -> Dict[str, Any]:
    """Build a JSON payload from UI string values."""

    payload: Dict[str, Any] = {}

    def add_str(key: str) -> None:
        v = (values.get(key) or "").strip()
        if v:
            payload[key] = v

    def add_float(key: str) -> None:
        v = (values.get(key) or "").strip()
        if not v:
            return
        try:
            payload[key] = float(v)
        except ValueError:
            raise ValueError(f"Điểm '{key}' không hợp lệ: '{v}'. Vui lòng nhập số từ 0-10.")

    if include_student_id:
        add_str("student_id")

    add_str("last_name")
    add_str("first_name")
    add_str("email")
    add_str("birth_date")
    add_str("hometown")

    for key in ("math_score", "literature_score", "english_score"):
        add_float(key)

    return payload
