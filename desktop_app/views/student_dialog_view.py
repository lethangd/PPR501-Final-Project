"""Student create/edit dialog view with ttkbootstrap."""

from __future__ import annotations

from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from ..components.modern_styles import ModernStyle


class StudentDialogView(ttk.Toplevel):
    """Modal dialog for creating/editing student."""
    
    def __init__(
        self, 
        parent: ttk.Window, 
        mode: str = "create", 
        student_data: Optional[dict] = None,
        on_save: Optional[callable] = None
    ):
        super().__init__(parent)
        
        self.mode = mode
        self.on_save = on_save
        self.result: Optional[dict] = None
        
        # Configure dialog
        self.title("Tạo sinh viên mới" if mode == "create" else "Chỉnh sửa sinh viên")
        self.geometry("520x700")
        self.resizable(True, True)
        self.minsize(520, 600)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        # Build UI
        self.vars: dict[str, ttk.StringVar] = {}
        self._build_ui(student_data)
    
    def _build_ui(self, student_data: Optional[dict]) -> None:
        """Build dialog UI with scrollable form."""
        # Main container with canvas for scrolling
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Canvas + Scrollbar
        canvas = ttk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=ModernStyle.PADDING_LG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        container = scrollable_frame
        
        # Title
        title = "Thêm sinh viên mới" if self.mode == "create" else "Chỉnh sửa thông tin"
        title_label = ttk.Label(
            container,
            text=title,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_H2, "bold"),
            foreground=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Form fields
        fields = [
            ("student_id", "Mã sinh viên", True),
            ("last_name", "Họ", False),
            ("first_name", "Tên", False),
            ("email", "Email", False),
            ("birth_date", "Ngày sinh (YYYY-MM-DD)", False),
            ("hometown", "Quê quán", False),
            ("math_score", "Điểm Toán (0-10)", False),
            ("literature_score", "Điểm Văn (0-10)", False),
            ("english_score", "Điểm Tiếng Anh (0-10)", False),
        ]
        
        for key, label, required in fields:
            self.vars[key] = ttk.StringVar()
            if student_data and key in student_data:
                value = student_data[key]
                self.vars[key].set(str(value) if value else "")
            
            # Label
            label_text = f"{label} {'*' if required else ''}"
            lbl = ttk.Label(
                container,
                text=label_text,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY),
                foreground=ModernStyle.TEXT_PRIMARY
            )
            lbl.pack(anchor="w", pady=(ModernStyle.PADDING_SM, 2))
            
            # Entry
            entry = ttk.Entry(
                container, 
                textvariable=self.vars[key], 
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY)
            )
            entry.pack(fill=X, pady=(0, 4))
            
            # Disable student_id if editing
            if key == "student_id" and self.mode == "edit":
                entry.configure(state="disabled")
        
        # Buttons - Fixed position at bottom (outside scrollable area)
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=X, pady=(24, 8))
        
        save_text = "Tạo mới" if self.mode == "create" else "Lưu thay đổi"
        ttk.Button(
            btn_frame,
            text=save_text,
            command=self._on_save_click,
            bootstyle="success",
            width=18
        ).pack(side=LEFT, padx=(0, 8))
        
        ttk.Button(
            btn_frame,
            text="Hủy",
            command=self._on_cancel,
            bootstyle="secondary-outline",
            width=18
        ).pack(side=LEFT)
    
    def _on_cancel(self) -> None:
        """Handle cancel button."""
        self.result = None
        self.destroy()
    
    def _on_save_click(self) -> None:
        """Handle save button."""
        # Collect data
        self.result = {}
        for key, var in self.vars.items():
            value = var.get().strip()
            if value:
                self.result[key] = value
        
        # Validate required fields
        if self.mode == "create" and "student_id" not in self.result:
            Messagebox.show_error("Mã sinh viên là bắt buộc!", "Lỗi", parent=self)
            return
        
        # Call callback if provided
        if self.on_save:
            try:
                self.on_save(self.result)
            except Exception as e:
                Messagebox.show_error(str(e), "Lỗi", parent=self)
                return
        
        self.destroy()
