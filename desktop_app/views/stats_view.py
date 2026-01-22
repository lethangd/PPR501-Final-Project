"""Statistics view component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..charts import build_figures
from ..components.modern_styles import ModernStyle
from ..models.student import Student
from ..xml_parser import StudentRecord


class StatsView(ttk.Frame):
    """Statistics view with charts."""
    
    def __init__(self, parent: tk.Misc):
        super().__init__(parent, style="TFrame")
        self._chart_canvases: List[FigureCanvasTkAgg] = []
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build UI."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Frame(self, style="TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ttk.Label(
            header,
            text="Thống kê & Phân tích",
            style="Title.TLabel"
        )
        title_label.pack(anchor="w")
        
        # Charts container
        chart_card = ttk.Frame(self, style="Card.TFrame", relief="solid", borderwidth=1)
        chart_card.grid(row=1, column=0, sticky="nsew")
        chart_card.columnconfigure(0, weight=1)
        chart_card.rowconfigure(0, weight=1)
        
        self._stats_canvas = tk.Canvas(chart_card, bg=ModernStyle.WHITE, highlightthickness=0)
        self._stats_scroll = ttk.Scrollbar(chart_card, orient="vertical", command=self._stats_canvas.yview)
        self._stats_canvas.configure(yscrollcommand=self._stats_scroll.set)
        
        self._stats_scroll.grid(row=0, column=1, sticky="ns")
        self._stats_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.chart_container = ttk.Frame(self._stats_canvas, style="Card.TFrame")
        self._stats_canvas.create_window((0, 0), window=self.chart_container, anchor="nw")
        
        self.chart_container.bind(
            "<Configure>",
            lambda _e: self._stats_canvas.configure(scrollregion=self._stats_canvas.bbox("all"))
        )
    
    def render_charts(self, students: List[Student]) -> None:
        """Render charts from student data."""
        # Clear existing charts
        for canvas in self._chart_canvases:
            canvas.get_tk_widget().destroy()
        self._chart_canvases.clear()
        
        # Convert Student to StudentRecord for charts
        records = [self._student_to_record(s) for s in students]
        
        # Build and render charts
        for fig in build_figures(records):
            canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=12)
            self._chart_canvases.append(canvas)
    
    @staticmethod
    def _student_to_record(student: Student) -> StudentRecord:
        """Convert Student model to StudentRecord.
        
        Note: StudentRecord expects string-typed scores for XML parsing,
        so we convert float/Decimal scores to strings.
        """
        def score_to_str(score) -> Optional[str]:
            """Convert numeric score to string, handling None."""
            if score is None:
                return None
            return str(float(score))
        
        return StudentRecord(
            student_id=student.student_id,
            last_name=student.last_name,
            first_name=student.first_name,
            email=student.email,
            birth_date=student.birth_date,
            hometown=student.hometown,
            math_score=score_to_str(student.math_score),
            literature_score=score_to_str(student.literature_score),
            english_score=score_to_str(student.english_score),
        )
