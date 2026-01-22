"""Student list view component with ttkbootstrap."""

from __future__ import annotations

from typing import List, Optional, Protocol

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ..components.modern_styles import Icons, ModernStyle
from ..models.student import PaginatedStudents, Student


class StudentListPresenter(Protocol):
    """Protocol for presenter."""
    
    def on_search(self, query: str) -> None: ...
    def on_create(self) -> None: ...
    def on_edit(self, student_id: str) -> None: ...
    def on_delete(self, student_id: str) -> None: ...
    def on_refresh(self) -> None: ...
    def on_page_change(self, page: int) -> None: ...


class StudentListView(ttk.Frame):
    """Student list view with table, search, and pagination."""
    
    def __init__(self, parent: tk.Misc, presenter: StudentListPresenter):
        super().__init__(parent, style="TFrame")
        self.presenter = presenter
        self.current_page = 0
        self.total_pages = 1
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build UI components."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        self._build_header()
        self._build_action_bar()
        self._build_table()
        self._build_pagination()
    
    def _build_header(self) -> None:
        """Build header section."""
        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky=EW, pady=(0, 20))
        header.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            header,
            text="Quản lý sinh viên",
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-dark"
        )
        title_label.grid(row=0, column=0, sticky=W)
        
        # Status
        self.status_var = ttk.StringVar(value="")
        status_label = ttk.Label(
            header,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        status_label.grid(row=0, column=1, sticky=E, padx=(10, 0))
    
    def _build_action_bar(self) -> None:
        """Build search and action bar - Search first, Create button last."""
        action_bar = ttk.Frame(self)
        action_bar.grid(row=1, column=0, sticky=EW, pady=(0, 16))
        action_bar.columnconfigure(0, weight=1)  # Search takes available space
        
        # Modern Search Entry - FIRST, takes most space (ttkbootstrap)
        self.search_var = ttk.StringVar()
        self.search_entry = ttk.Entry(
            action_bar,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            width=50
        )
        self.search_entry.grid(row=0, column=0, sticky=EW, padx=(0, 12))
        self.search_entry.insert(0, f"{Icons.SEARCH} Tìm kiếm theo tên, mã sinh viên, email...")
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change())
        self.search_entry.config(foreground="gray")
        
        # Create Button - LAST, green color (ttkbootstrap style)
        create_btn = ttk.Button(
            action_bar,
            text=f"{Icons.ADD} Tạo mới sinh viên",
            command=lambda: self.presenter.on_create(),
            bootstyle="success",  # Green ttkbootstrap style!
            width=20
        )
        create_btn.grid(row=0, column=1, sticky=E)
    
    def _build_table(self) -> None:
        """Build table with glassmorphism card."""
        # Table container (ttkbootstrap Frame)
        table_card = ttk.Frame(self, bootstyle="light")
        table_card.grid(row=2, column=0, sticky=NSEW)
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)
        table_container = table_card
        
        # Define columns - narrower score columns
        columns = ["student_id", "last_name", "first_name", "email", "hometown", 
                   "math_score", "literature_score", "english_score", "actions"]
        
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="none",
            bootstyle="primary",  # ttkbootstrap style
            height=25  # Increased for full screen
        )
        
        # Configure columns
        headings = {
            "student_id": "Mã SV",
            "last_name": "Họ",
            "first_name": "Tên",
            "email": "Email",
            "hometown": "Quê quán",
            "math_score": "Toán",
            "literature_score": "Văn",
            "english_score": "Anh",
            "actions": "Thao tác"
        }
        
        # Narrower widths for score columns
        widths = {
            "student_id": 100,
            "last_name": 130,
            "first_name": 130,
            "email": 220,
            "hometown": 140,
            "math_score": 60,  # Narrower
            "literature_score": 60,  # Narrower
            "english_score": 60,  # Narrower
            "actions": 180
        }
        
        for col in columns:
            self.tree.heading(col, text=headings.get(col, col))
            self.tree.column(
                col, 
                width=widths.get(col, 100), 
            anchor=CENTER if col in ["math_score", "literature_score", "english_score"] else W,
            stretch=YES if col not in ["math_score", "literature_score", "english_score", "actions"] else NO
            )
        
        # Configure alternating row colors (zebra striping)
        self.tree.tag_configure("oddrow", background="#F8F9FA")  # Light gray
        self.tree.tag_configure("evenrow", background="#FFFFFF")  # White
        
        # Configure tree style - LARGER fonts and row height
        style = ttk.Style()
        style.configure("Treeview", 
            rowheight=50,  # Increased for better readability
            font=("Segoe UI", 12)  # Larger font
        )
        style.configure("Treeview.Heading",
            font=("Segoe UI", 13, "bold"),  # Larger header font
            padding=10
        )
        
        # Scrollbars
        yscroll = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_container, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=NSEW)
        yscroll.grid(row=0, column=1, sticky=NS)
        xscroll.grid(row=1, column=0, sticky=EW)
        
        # Bind single-click for edit/delete actions
        self.tree.bind("<Button-1>", self._on_tree_click)
    
    def _build_pagination(self) -> None:
        """Build pagination controls."""
        pagination_frame = ttk.Frame(self)
        pagination_frame.grid(row=3, column=0, sticky=EW, pady=(16, 0))
        pagination_frame.columnconfigure(1, weight=1)
        
        # Page info
        self.page_info_var = ttk.StringVar(value="")
        page_info_label = ttk.Label(
            pagination_frame,
            textvariable=self.page_info_var,
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        page_info_label.grid(row=0, column=0, sticky=W)
        
        # Page controls with ttkbootstrap buttons
        page_controls = ttk.Frame(pagination_frame)
        page_controls.grid(row=0, column=1, sticky=E)
        
        self.prev_btn = ttk.Button(
            page_controls,
            text=f"{Icons.ARROW_LEFT} Trước",
            command=self._prev_page,
            bootstyle="info",  # Solid blue - much clearer!
            width=12
        )
        self.prev_btn.pack(side=LEFT, padx=(0, 8))
        
        self.page_label_var = ttk.StringVar(value="")
        page_label = ttk.Label(
            page_controls,
            textvariable=self.page_label_var,
            font=("Segoe UI", 12, "bold"),
            bootstyle="dark"
        )
        page_label.pack(side=LEFT, padx=(0, 8))
        
        self.next_btn = ttk.Button(
            page_controls,
            text=f"Sau {Icons.ARROW_RIGHT}",
            command=self._next_page,
            bootstyle="info",  # Solid blue - much clearer!
            width=12
        )
        self.next_btn.pack(side=LEFT)
    
    # Event handlers
    
    def _on_search_focus_in(self, event) -> None:
        """Handle search focus in."""
        placeholder = f"{Icons.SEARCH} Tìm kiếm theo tên, mã sinh viên, email..."
        if self.search_entry.get() == placeholder:
            self.search_entry.delete(0, END)
            self.search_entry.config(foreground="black")
    
    def _on_search_focus_out(self, event) -> None:
        """Handle search focus out."""
        if not self.search_entry.get():
            placeholder = f"{Icons.SEARCH} Tìm kiếm theo tên, mã sinh viên, email..."
            self.search_entry.insert(0, placeholder)
            self.search_entry.config(foreground="gray")
    
    def _on_search_change(self) -> None:
        """Handle search change."""
        query = self.search_var.get()
        placeholder = f"{Icons.SEARCH} Tìm kiếm theo tên, mã sinh viên, email..."
        if query == placeholder:
            query = ""
        self.presenter.on_search(query)
    
    def _on_tree_click(self, event) -> None:
        """Handle tree single-click for edit/delete actions."""
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        column = self.tree.identify_column(event.x)
        col_index = int(column.replace("#", "")) - 1
        
        if col_index == 8:  # Actions column
            x = event.x
            bbox = self.tree.bbox(item, column)
            if not bbox:
                return
            col_x = bbox[0]
            relative_x = x - col_x
            col_width = self.tree.column(column, "width")
            
            if relative_x < col_width // 2:
                self.presenter.on_edit(item)
            else:
                self.presenter.on_delete(item)
        else:
            self.presenter.on_edit(item)
    
    def _prev_page(self) -> None:
        """Go to previous page."""
        if self.current_page > 0:
            self.presenter.on_page_change(self.current_page - 1)
    
    def _next_page(self) -> None:
        """Go to next page."""
        if self.current_page < self.total_pages - 1:
            self.presenter.on_page_change(self.current_page + 1)
    
    # Public methods for presenter
    
    def render_students(self, paginated: PaginatedStudents) -> None:
        """Render students in table."""
        # Clear existing
        self.tree.delete(*self.tree.get_children())
        
        # Update pagination state
        self.current_page = paginated.page
        self.total_pages = paginated.total_pages
        
        # Render rows with alternating colors
        for idx, student in enumerate(paginated.students):
            values = [
                student.student_id,
                student.last_name or "",
                student.first_name or "",
                student.email or "",
                student.hometown or "",
                self._format_score(student.math_score),
                self._format_score(student.literature_score),
                self._format_score(student.english_score),
                "✏️  Sửa  |  🗑️  Xóa"
            ]
            # Alternate row colors
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", END, iid=student.student_id, values=values, tags=(tag,))
        
        # Update pagination controls
        self._update_pagination_info(paginated)
    
    def set_status(self, text: str) -> None:
        """Set status text."""
        self.status_var.set(text)
    
    def _format_score(self, score: Optional[float]) -> str:
        """Format score for display."""
        if score is None:
            return ""
        try:
            return f"{float(score):.1f}"
        except (ValueError, TypeError):
            return str(score) if score else ""
    
    def _update_pagination_info(self, paginated: PaginatedStudents) -> None:
        """Update pagination info."""
        # Page label
        self.page_label_var.set(f"Trang {paginated.page + 1} / {paginated.total_pages}")
        
        # Page info
        start = paginated.page * paginated.page_size + 1 if paginated.total > 0 else 0
        end = min((paginated.page + 1) * paginated.page_size, paginated.total)
        self.page_info_var.set(f"Hiển thị {start}-{end} trong tổng số {paginated.total} sinh viên")
        
        # Button states - Fix logic to enable/disable correctly
        # Enable prev if NOT on first page
        if paginated.page > 0:
            self.prev_btn.state(["!disabled"])
        else:
            self.prev_btn.state(["disabled"])
        
        # Enable next if NOT on last page
        if paginated.page < paginated.total_pages - 1:
            self.next_btn.state(["!disabled"])
        else:
            self.next_btn.state(["disabled"])
