"""Student list presenter (business logic)."""

from __future__ import annotations

import threading
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..views.student_list_view import StudentListView

from ..services.student_service import StudentService


class StudentListPresenter:
    """Presenter for student list (MVP pattern)."""
    
    def __init__(self, view: StudentListView, service: StudentService, root_window, api_base_url: str = "http://localhost:8000/api"):
        self.view = view
        self.service = service
        self.root_window = root_window
        self.api_base_url = api_base_url
        
        self.current_page = 0
        self.search_query = ""
    
    def load_data(self) -> None:
        """Load initial data."""
        self._load_page()
    
    def on_search(self, query: str) -> None:
        """Handle search query change."""
        self.search_query = query
        self.current_page = 0
        self._load_page()
    
    def on_create(self) -> None:
        """Handle create button click."""
        from ..views.student_dialog_view import StudentDialogView
        
        dialog = StudentDialogView(
            self.root_window,
            mode="create",
            on_save=self._handle_create,
            api_base_url=self.api_base_url
        )
        self.root_window.wait_window(dialog)
    
    def on_edit(self, student_id: str) -> None:
        """Handle edit click."""
        from ..views.student_dialog_view import StudentDialogView
        
        # Get student data
        paginated = self.service.get_paginated(
            page=self.current_page,
            page_size=25,
            search_query=self.search_query
        )
        student = next((s for s in paginated.students if s.student_id == student_id), None)
        if not student:
            return
        
        dialog = StudentDialogView(
            self.root_window,
            mode="edit",
            student_data=student.to_dict(),
            on_save=lambda data: self._handle_update(student_id, data),
            api_base_url=self.api_base_url
        )
        self.root_window.wait_window(dialog)
    
    def on_delete(self, student_id: str) -> None:
        """Handle delete click."""
        if messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa sinh viên {student_id}?",
            parent=self.root_window
        ):
            self._delete_student(student_id)
    
    
    def on_page_change(self, page: int) -> None:
        """Handle page change."""
        self.current_page = page
        self._load_page()
    
    # Private methods
    
    def _load_page(self) -> None:
        """Load current page data."""
        self.view.set_status("Đang tải...")
        
        def work():
            try:
                paginated = self.service.get_paginated(
                    page=self.current_page,
                    page_size=25,
                    search_query=self.search_query
                )
                self.view.after(0, lambda: self._on_data_loaded(paginated))
            except Exception as e:
                self.view.after(0, lambda: self._on_error(f"Lỗi tải dữ liệu: {e}"))
        
        threading.Thread(target=work, daemon=True).start()
    
    def _on_data_loaded(self, paginated) -> None:
        """Handle data loaded."""
        self.view.render_students(paginated)
        self.view.set_status(f"Đã tải {paginated.total} sinh viên")
    
    def _handle_create(self, data: dict) -> None:
        """Handle create student."""
        self.view.set_status("Đang tạo...")
        
        def work():
            try:
                self.service.create(data)
                self.view.after(0, self._load_page)
            except Exception as e:
                self.view.after(0, lambda: self._on_error(f"Lỗi tạo: {e}"))
        
        threading.Thread(target=work, daemon=True).start()
    
    def _handle_update(self, student_id: str, data: dict) -> None:
        """Handle update student."""
        self.view.set_status("Đang cập nhật...")
        
        def work():
            try:
                self.service.update(student_id, data)
                self.view.after(0, self._load_page)
            except Exception as e:
                self.view.after(0, lambda: self._on_error(f"Lỗi cập nhật: {e}"))
        
        threading.Thread(target=work, daemon=True).start()
    
    def _delete_student(self, student_id: str) -> None:
        """Delete student."""
        self.view.set_status("Đang xóa...")
        
        def work():
            try:
                self.service.delete(student_id)
                self.view.after(0, self._load_page)
            except Exception as e:
                self.view.after(0, lambda: self._on_error(f"Lỗi xóa: {e}"))
        
        threading.Thread(target=work, daemon=True).start()
    
    def _on_error(self, message: str) -> None:
        """Handle error."""
        self.view.set_status("Lỗi")
        messagebox.showerror("Lỗi", message, parent=self.root_window)
