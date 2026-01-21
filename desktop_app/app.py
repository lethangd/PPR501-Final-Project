"""Tkinter Desktop App - Student Management System."""

from __future__ import annotations

import argparse
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .charts import build_figure
from .student_api import ApiError, StudentApiClient
from .xml_parser import StudentRecord, to_api_payload


class StudentApp(ttk.Frame):
    """Main UI container."""

    def __init__(self, master: tk.Misc, api: StudentApiClient) -> None:
        super().__init__(master)
        self.api = api

        self.vars: Dict[str, tk.StringVar] = {
            key: tk.StringVar(value="") for key in StudentRecord.columns()
        }

        self._build_layout()
        self._bind_events()

        self.refresh_students_async()

    def _build_layout(self) -> None:
        self.master.title("Student Management System (Tkinter)")
        self.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=(10, 6))

        ttk.Button(toolbar, text="Tải lại", command=self.refresh_students_async).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Tạo mới", command=self.create_student_async).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(toolbar, text="Cập nhật", command=self.update_student_async).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(toolbar, text="Xóa", command=self.delete_student_async).pack(side=tk.LEFT, padx=(6, 0))

        self.status_var = tk.StringVar(value="Sẵn sàng")
        ttk.Label(toolbar, textvariable=self.status_var).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        data_tab = ttk.Frame(self.notebook)
        stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(data_tab, text="Danh sách")
        self.notebook.add(stats_tab, text="Thống kê")

        self._build_data_tab(data_tab)
        self._build_stats_tab(stats_tab)

    def _build_data_tab(self, parent: ttk.Frame) -> None:
        body = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True)

        table_frame = ttk.Frame(body)
        form_frame = ttk.Frame(body)
        body.add(table_frame, weight=3)
        body.add(form_frame, weight=2)

        self._build_table(table_frame)
        self._build_form(form_frame)

    def _build_stats_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self.chart_container = ttk.Frame(parent)
        self.chart_container.grid(row=0, column=0, sticky="nsew")

        self._chart_canvas: FigureCanvasTkAgg | None = None
        self._render_charts([])

    def _build_table(self, parent: ttk.Frame) -> None:
        columns = StudentRecord.columns()

        self.tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "student_id": "Mã SV",
            "last_name": "Họ",
            "first_name": "Tên",
            "email": "Email",
            "birth_date": "Ngày sinh",
            "hometown": "Quê quán",
            "math_score": "Toán",
            "literature_score": "Văn",
            "english_score": "Anh",
        }
        widths = {
            "student_id": 90,
            "last_name": 120,
            "first_name": 120,
            "email": 200,
            "birth_date": 110,
            "hometown": 130,
            "math_score": 70,
            "literature_score": 70,
            "english_score": 70,
        }

        for col in columns:
            self.tree.heading(col, text=headings.get(col, col))
            self.tree.column(col, width=widths.get(col, 120), anchor=tk.W)

        yscroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        xscroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

    def _build_form(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)

        ttk.Label(parent, text="Thông tin sinh viên", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(6, 10)
        )

        row = 1
        for key, label in [
            ("student_id", "Mã SV *"),
            ("last_name", "Họ"),
            ("first_name", "Tên"),
            ("email", "Email"),
            ("birth_date", "Ngày sinh (YYYY-MM-DD)"),
            ("hometown", "Quê quán"),
            ("math_score", "Điểm Toán"),
            ("literature_score", "Điểm Văn"),
            ("english_score", "Điểm Anh"),
        ]:
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
            entry = ttk.Entry(parent, textvariable=self.vars[key])
            entry.grid(row=row, column=1, sticky="ew", pady=3)
            row += 1

        ttk.Separator(parent).grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        ttk.Button(parent, text="Clear form", command=self.clear_form).grid(
            row=row, column=0, columnspan=2, sticky="ew"
        )

        ttk.Label(
            parent,
            text="Mẹo: Click một dòng bên trái để nạp dữ liệu vào form.",
            foreground="#555",
        ).grid(row=row + 1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _bind_events(self) -> None:
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _on_row_select(self, _event: tk.Event) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")

        for key, value in zip(StudentRecord.columns(), values):
            self.vars[key].set(value)

    def clear_form(self) -> None:
        for var in self.vars.values():
            var.set("")

    # Async helpers

    def _set_status(self, text: str) -> None:
        self.status_var.set(text)

    def refresh_students_async(self) -> None:
        self._set_status("Đang tải danh sách...")

        def work() -> None:
            try:
                students = self.api.list_students()
                self.after(0, lambda: self._render_students(students))
                self.after(0, lambda: self._render_charts(students))
                self.after(0, lambda: self._set_status(f"Đã tải {len(students)} sinh viên"))
            except ApiError as e:
                self.after(0, lambda: self._show_api_error(e))

        threading.Thread(target=work, daemon=True).start()

    def create_student_async(self) -> None:
        values = {k: v.get() for k, v in self.vars.items()}
        try:
            payload = to_api_payload(values, include_student_id=True)
        except ValueError:
            messagebox.showerror("Lỗi", "Điểm phải là số (0-10)")
            return

        if not payload.get("student_id"):
            messagebox.showwarning("Thiếu dữ liệu", "Mã SV là bắt buộc")
            return

        self._set_status("Đang tạo sinh viên...")

        def work() -> None:
            try:
                self.api.create_student(payload)
                self.after(0, self.refresh_students_async)
                self.after(0, self.clear_form)
            except ApiError as e:
                self.after(0, lambda: self._show_api_error(e))

        threading.Thread(target=work, daemon=True).start()

    def update_student_async(self) -> None:
        student_id = self.vars["student_id"].get().strip()
        if not student_id:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn sinh viên hoặc nhập Mã SV")
            return

        values = {k: v.get() for k, v in self.vars.items()}
        try:
            payload = to_api_payload(values, include_student_id=False)
        except ValueError:
            messagebox.showerror("Lỗi", "Điểm phải là số (0-10)")
            return

        if not payload:
            messagebox.showinfo("Không có thay đổi", "Không có trường nào để cập nhật")
            return

        self._set_status("Đang cập nhật...")

        def work() -> None:
            try:
                self.api.update_student(student_id, payload)
                self.after(0, self.refresh_students_async)
            except ApiError as e:
                self.after(0, lambda: self._show_api_error(e))

        threading.Thread(target=work, daemon=True).start()

    def delete_student_async(self) -> None:
        student_id = self.vars["student_id"].get().strip()
        if not student_id:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn sinh viên hoặc nhập Mã SV")
            return

        if not messagebox.askyesno("Xác nhận", f"Xóa sinh viên {student_id}?"):
            return

        self._set_status("Đang xóa...")

        def work() -> None:
            try:
                self.api.delete_student(student_id)
                self.after(0, self.refresh_students_async)
                self.after(0, self.clear_form)
            except ApiError as e:
                self.after(0, lambda: self._show_api_error(e))

        threading.Thread(target=work, daemon=True).start()

    def _render_students(self, students: list[StudentRecord]) -> None:
        self.tree.delete(*self.tree.get_children())

        for s in students:
            self.tree.insert("", tk.END, iid=s.student_id, values=s.to_row())

    def _render_charts(self, students: list[StudentRecord]) -> None:
        fig = build_figure(students)

        if self._chart_canvas is not None:
            self._chart_canvas.get_tk_widget().destroy()

        self._chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _show_api_error(self, err: ApiError) -> None:
        self._set_status("Lỗi")

        msg = err.message
        if err.details:
            msg = f"{msg}\n\nChi tiết: {err.details}"

        messagebox.showerror("API Error", msg)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        default="http://localhost:8000/api",
        help="Base API URL (default: http://localhost:8000/api)",
    )
    args = parser.parse_args()

    api = StudentApiClient(base_url=args.api)

    root = tk.Tk()
    root.geometry("1100x650")

    style = ttk.Style(root)
    # 'vista' looks good on Windows; fallback is handled by Tk.
    try:
        style.theme_use("vista")
    except tk.TclError:
        pass
    style.configure("Treeview", rowheight=24)
    style.configure("TButton", padding=6)

    app = StudentApp(root, api)

    def on_close() -> None:
        api.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
