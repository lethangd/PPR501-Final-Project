"""Main application - Student Management System (MVP Architecture with ttkbootstrap)."""

from __future__ import annotations

import argparse

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .components.modern_styles import ModernStyle
from .presenters.student_list_presenter import StudentListPresenter
from .services.student_service import StudentService
from .student_api import StudentApiClient
from .views.stats_view import StatsView
from .views.student_list_view import StudentListView


class StudentApp(ttk.Frame):
    """
    Main application using MVP (Model-View-Presenter) pattern.
    
    Architecture:
    - Models (models/): Data structures (Student, PaginatedStudents)
    - Views (views/): UI components (StudentListView, StatsView, StudentDialogView)
    - Presenters (presenters/): Business logic (StudentListPresenter)
    - Services (services/): API communication (StudentService)
    - Components (components/): Shared utilities (ModernStyle)
    """
    
    def __init__(self, master: ttk.Window, api_client: StudentApiClient):
        super().__init__(master)
        self.api_client = api_client
        
        # Setup styles
        self._setup_styles()
        
        # Initialize services
        self.student_service = StudentService(api_client)
        
        # Build UI
        self._build_ui()
        
        # Load initial data
        self.student_list_presenter.load_data()
        self._load_stats()
    
    def _setup_styles(self) -> None:
        """Configure ttkbootstrap styles (already beautiful by default!)."""
        # ttkbootstrap handles most styling automatically
        # Themes: flatly, darkly, cosmo, journal, litera, lumen, minty, pulse, sandstone, superhero, yeti
        # We only need minor customizations
        pass
    
    def _build_ui(self) -> None:
        """Build modern ttkbootstrap UI."""
        self.master.title("🎓 Hệ thống Quản lý Sinh viên")
        self.pack(fill=BOTH, expand=YES)
        
        # Main container with generous padding
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Notebook (tabs) with bootstrap styling
        self.notebook = ttk.Notebook(main_container, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)
        
        # Student List Tab (MVP: View + Presenter)
        self.student_list_view = StudentListView(self.notebook, presenter=None)  # Temp
        self.student_list_presenter = StudentListPresenter(
            view=self.student_list_view,
            service=self.student_service,
            root_window=self.master
        )
        # Inject presenter after creation
        self.student_list_view.presenter = self.student_list_presenter
        
        self.notebook.add(self.student_list_view, text="📋 Danh sách sinh viên")
        
        # Statistics Tab
        self.stats_view = StatsView(self.notebook)
        self.notebook.add(self.stats_view, text="📊 Thống kê")
        
        # Bind tab change to reload stats
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    
    def _on_tab_changed(self, event) -> None:
        """Handle tab change."""
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:  # Stats tab
            self._load_stats()
    
    def _load_stats(self) -> None:
        """Load statistics data."""
        import threading
        
        def work():
            try:
                students = self.student_service.get_all_for_stats()
                self.stats_view.after(0, lambda: self.stats_view.render_charts(students))
            except Exception as e:
                print(f"Error loading stats: {e}")
        
        threading.Thread(target=work, daemon=True).start()


def main() -> None:
    """
    Main entry point.
    
    Architecture Overview:
    =====================
    
    MVP Pattern:
    -----------
    - Model: Data structures (Student, PaginatedStudents)
    - View: UI components (StudentListView, StatsView)
    - Presenter: Business logic (StudentListPresenter)
    
    Layers:
    -------
    1. Views (views/): Pure UI, no business logic
    2. Presenters (presenters/): Handle user actions, coordinate views and services
    3. Services (services/): API communication with caching
    4. Models (models/): Data structures
    5. Components (components/): Shared utilities
    
    Data Flow:
    ---------
    User Action → View → Presenter → Service → API
                    ↑                    ↓
                    └────── Update ──────┘
    
    Benefits:
    --------
    - Separation of concerns
    - Testable business logic
    - Reusable components
    - Clear data flow
    - Easy to extend
    """
    parser = argparse.ArgumentParser(
        description="Student Management System (MVP Architecture)"
    )
    parser.add_argument(
        "--api",
        default="http://localhost:8000/api",
        help="Base API URL (default: http://localhost:8000/api)",
    )
    args = parser.parse_args()
    
    # Initialize API client
    api = StudentApiClient(base_url=args.api)
    
    # Create ttkbootstrap window with modern theme
    # Themes: flatly, darkly, cosmo, journal, litera, lumen, minty, pulse, sandstone, superhero, yeti
    root = ttk.Window(
        title="🎓 Hệ thống Quản lý Sinh viên",
        themename="flatly",  # Modern light theme (can try: superhero, darkly)
        size=(1400, 800),
        minsize=(1200, 700)
    )
    
    # Create app
    app = StudentApp(root, api)
    
    # Handle close
    def on_close() -> None:
        api.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Start
    root.mainloop()


if __name__ == "__main__":
    main()
