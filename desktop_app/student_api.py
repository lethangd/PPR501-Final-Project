"""HTTP client for the Student API (XML responses)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from .xml_parser import StudentRecord, parse_students_xml


DEFAULT_BASE_URL = "http://localhost:8000/api"


@dataclass
class ApiError(Exception):
    """API/connection error with user-facing message."""

    message: str
    status_code: Optional[int] = None
    details: Optional[str] = None


class StudentApiClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: tuple[float, float] = (3.05, 30.0),
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def close(self) -> None:
        self._session.close()

    def list_students(self) -> List[StudentRecord]:
        url = f"{self.base_url}/students"
        try:
            resp = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return parse_students_xml(resp.text)
        except requests.exceptions.RequestException as e:
            raise self._wrap_error("Không thể lấy danh sách sinh viên", e)
        except ValueError as e:
            raise ApiError("Dữ liệu XML không hợp lệ", details=str(e))

    def get_student(self, student_id: str) -> StudentRecord:
        url = f"{self.base_url}/students/{student_id}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            records = parse_students_xml(resp.text)
            return records[0]
        except requests.exceptions.RequestException as e:
            raise self._wrap_error(f"Không thể lấy sinh viên {student_id}", e)
        except (ValueError, IndexError) as e:
            raise ApiError("Dữ liệu XML không hợp lệ", details=str(e))

    def create_student(self, payload: Dict[str, Any]) -> StudentRecord:
        url = f"{self.base_url}/students"
        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return parse_students_xml(resp.text)[0]
        except requests.exceptions.RequestException as e:
            raise self._wrap_error("Tạo sinh viên thất bại", e)
        except (ValueError, IndexError) as e:
            raise ApiError("Dữ liệu XML không hợp lệ", details=str(e))

    def update_student(self, student_id: str, payload: Dict[str, Any]) -> StudentRecord:
        url = f"{self.base_url}/students/{student_id}"
        try:
            resp = self._session.put(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return parse_students_xml(resp.text)[0]
        except requests.exceptions.RequestException as e:
            raise self._wrap_error(f"Cập nhật sinh viên {student_id} thất bại", e)
        except (ValueError, IndexError) as e:
            raise ApiError("Dữ liệu XML không hợp lệ", details=str(e))

    def delete_student(self, student_id: str) -> None:
        url = f"{self.base_url}/students/{student_id}"
        try:
            resp = self._session.delete(url, timeout=self.timeout)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise self._wrap_error(f"Xóa sinh viên {student_id} thất bại", e)

    def _wrap_error(self, prefix: str, exc: requests.exceptions.RequestException) -> ApiError:
        status_code: Optional[int] = None
        details: Optional[str] = None

        # If we have a Response, surface useful details.
        if isinstance(exc, requests.exceptions.HTTPError) and exc.response is not None:
            status_code = exc.response.status_code
            try:
                # FastAPI errors are usually JSON: {"detail": "..."}
                data = exc.response.json()
                if isinstance(data, dict) and "detail" in data:
                    details = str(data["detail"])
                else:
                    details = exc.response.text
            except Exception:
                details = exc.response.text

        # Connection errors/timeouts -> message without status.
        msg = prefix
        if status_code is not None:
            msg = f"{prefix} (HTTP {status_code})"

        return ApiError(message=msg, status_code=status_code, details=details)
