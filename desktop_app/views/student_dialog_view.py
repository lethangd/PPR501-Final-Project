"""Student create/edit dialog view with ttkbootstrap."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from ..components.modern_styles import ModernStyle
from ..province_api import Province, ProvinceApiClient


class StudentDialogView(ttk.Toplevel):
    """Modal dialog for creating/editing student."""
    
    def __init__(
        self, 
        parent: ttk.Window, 
        mode: str = "create", 
        student_data: Optional[dict] = None,
        on_save: Optional[callable] = None,
        api_base_url: str = "http://localhost:8000/api"
    ):
        super().__init__(parent)
        
        self.mode = mode
        self.on_save = on_save
        self.result: Optional[dict] = None
        self.api_base_url = api_base_url
        
        # Province data
        self.province_api = ProvinceApiClient(api_base_url)
        self.provinces: list[Province] = []
        self.selected_province_id: Optional[int] = None
        
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
        
        # Form fields - Text inputs
        text_fields = [
            ("student_id", "Mã sinh viên", True),
            ("last_name", "Họ", False),
            ("first_name", "Tên", False),
            ("email", "Email", False),
        ]
        
        for key, label, required in text_fields:
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
        
        # Birth Date - Date Picker (Special Widget)
        self.vars["birth_date"] = ttk.StringVar()
        
        lbl = ttk.Label(
            container,
            text="Ngày sinh",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY),
            foreground=ModernStyle.TEXT_PRIMARY
        )
        lbl.pack(anchor="w", pady=(ModernStyle.PADDING_SM, 2))
        
        # Date picker frame
        date_frame = ttk.Frame(container)
        date_frame.pack(fill=X, pady=(0, 4))
        
        try:
            from ttkbootstrap.widgets import DateEntry
            
            # Get initial date
            initial_date = None
            if student_data and "birth_date" in student_data and student_data["birth_date"]:
                try:
                    initial_date = datetime.strptime(str(student_data["birth_date"]), "%Y-%m-%d")
                except ValueError:
                    pass
            
            # DateEntry widget with calendar popup
            self.date_entry = DateEntry(
                date_frame,
                bootstyle="primary",
                dateformat="%Y-%m-%d",
                firstweekday=0,  # Monday
                startdate=initial_date
            )
            self.date_entry.pack(side=LEFT, fill=X, expand=YES)
            
            # Clear button
            ttk.Button(
                date_frame,
                text="✕",
                bootstyle="secondary-outline",
                width=3,
                command=lambda: self.date_entry.entry.delete(0, END)
            ).pack(side=LEFT, padx=(4, 0))
            
        except ImportError:
            # Fallback to regular Entry if DateEntry not available
            entry = ttk.Entry(
                date_frame, 
                textvariable=self.vars["birth_date"], 
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY)
            )
            entry.pack(fill=X)
            if student_data and "birth_date" in student_data:
                value = student_data["birth_date"]
                self.vars["birth_date"].set(str(value) if value else "")
        
        # Province - Combobox with Autocomplete
        lbl = ttk.Label(
            container,
            text="Tỉnh/Thành phố",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY),
            foreground=ModernStyle.TEXT_PRIMARY
        )
        lbl.pack(anchor="w", pady=(ModernStyle.PADDING_SM, 2))
        
        # Load provinces from API
        try:
            self.provinces = self.province_api.list_all()
        except Exception as e:
            print(f"Error loading provinces: {e}")
            self.provinces = []
        
        # Province names for combobox
        province_names = [p.name for p in self.provinces]
        
        # Combobox for province selection
        self.province_var = ttk.StringVar()
        self.province_combo = ttk.Combobox(
            container,
            textvariable=self.province_var,
            values=province_names,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY),
            state="readonly"  # Only allow selection from list
        )
        self.province_combo.pack(fill=X, pady=(0, 4))
        
        # Set initial value if editing
        if student_data and "province_name" in student_data and student_data["province_name"]:
            province_name = student_data["province_name"]
            if province_name in province_names:
                self.province_var.set(province_name)
                # Set selected_province_id
                for p in self.provinces:
                    if p.name == province_name:
                        self.selected_province_id = p.id
                        break
        elif student_data and "province_id" in student_data and student_data["province_id"]:
            # Fallback: lookup by ID
            province_id = student_data["province_id"]
            for p in self.provinces:
                if p.id == province_id:
                    self.province_var.set(p.name)
                    self.selected_province_id = p.id
                    break
        
        # Bind selection event
        self.province_combo.bind("<<ComboboxSelected>>", self._on_province_selected)
        
        # Score fields
        score_fields = [
            ("math_score", "Điểm Toán (0-10)", False),
            ("literature_score", "Điểm Văn (0-10)", False),
            ("english_score", "Điểm Tiếng Anh (0-10)", False),
        ]
        
        for key, label, required in score_fields:
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
    
    def _on_province_selected(self, event) -> None:
        """Handle province selection from combobox."""
        selected_name = self.province_var.get()
        for p in self.provinces:
            if p.name == selected_name:
                self.selected_province_id = p.id
                break
    
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
        
        # Get birth_date from DateEntry if available
        if hasattr(self, 'date_entry'):
            try:
                date_str = self.date_entry.entry.get().strip()
                if date_str:
                    self.result["birth_date"] = date_str
            except Exception:
                pass
        
        # Get province_id from selected province
        if self.selected_province_id:
            self.result["province_id"] = self.selected_province_id
            # Also include province_name for backward compatibility
            selected_name = self.province_var.get()
            if selected_name:
                self.result["hometown"] = selected_name
        
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
