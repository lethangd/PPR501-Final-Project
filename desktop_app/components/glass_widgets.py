"""Custom widgets with Glassmorphism effects."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .modern_styles import ModernStyle, Icons


class GlassCard(tk.Frame):
    """
    Card with glassmorphism effect.
    
    Features:
    - Rounded corners (simulated)
    - Soft shadows
    - White/transparent background
    - Subtle border
    """
    
    def __init__(
        self, 
        parent,
        padding: int = ModernStyle.PADDING_LG,
        radius: int = ModernStyle.RADIUS_MD,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=ModernStyle.SURFACE,
            highlightbackground=ModernStyle.GLASS_BORDER,
            highlightthickness=1,
            highlightcolor=ModernStyle.GLASS_BORDER,
        )
        
        # Inner frame for content with padding
        self.content = tk.Frame(self, bg=ModernStyle.SURFACE)
        self.content.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)


class ModernButton(tk.Button):
    """
    Modern button with hover effects.
    
    Variants:
    - primary: Purple gradient
    - secondary: Light gray
    - danger: Red
    - success: Green
    """
    
    def __init__(
        self,
        parent,
        text: str = "",
        command=None,
        variant: str = "primary",
        icon: str = "",
        **kwargs
    ):
        # Color mapping
        colors = {
            "primary": {
                "bg": ModernStyle.PRIMARY,
                "fg": ModernStyle.TEXT_ON_PRIMARY,
                "hover_bg": ModernStyle.PRIMARY_DARK,
                "active_bg": ModernStyle.PRIMARY_DARK,
            },
            "secondary": {
                "bg": ModernStyle.BACKGROUND_DARK,
                "fg": ModernStyle.TEXT_PRIMARY,
                "hover_bg": ModernStyle.BORDER,
                "active_bg": ModernStyle.BORDER,
            },
            "danger": {
                "bg": ModernStyle.DANGER,
                "fg": ModernStyle.TEXT_ON_PRIMARY,
                "hover_bg": "#DC2626",  # Red-600
                "active_bg": "#B91C1C",  # Red-700
            },
            "success": {
                "bg": ModernStyle.SUCCESS,
                "fg": ModernStyle.TEXT_ON_PRIMARY,
                "hover_bg": "#059669",  # Emerald-600
                "active_bg": "#047857",  # Emerald-700
            },
        }
        
        style = colors.get(variant, colors["primary"])
        
        # Add icon to text
        display_text = f"{icon} {text}" if icon else text
        
        super().__init__(
            parent,
            text=display_text,
            command=command,
            bg=style["bg"],
            fg=style["fg"],
            activebackground=style["active_bg"],
            activeforeground=style["fg"],
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY, "bold"),
            relief=tk.FLAT,
            borderwidth=0,
            padx=ModernStyle.PADDING_LG,
            pady=ModernStyle.PADDING_SM,
            cursor="hand2",
            **kwargs
        )
        
        # Hover effects
        self.bind("<Enter>", lambda e: self.configure(bg=style["hover_bg"]))
        self.bind("<Leave>", lambda e: self.configure(bg=style["bg"]))


class SearchEntry(tk.Frame):
    """Modern search input with icon."""
    
    def __init__(self, parent, textvariable=None, placeholder: str = "Search...", **kwargs):
        super().__init__(parent, bg=ModernStyle.SURFACE)
        
        # Container with border
        container = tk.Frame(
            self,
            bg=ModernStyle.SURFACE,
            highlightbackground=ModernStyle.BORDER,
            highlightthickness=1,
        )
        container.pack(fill=tk.BOTH, expand=True)
        
        # Search icon
        icon_label = tk.Label(
            container,
            text=Icons.SEARCH,
            bg=ModernStyle.SURFACE,
            fg=ModernStyle.TEXT_HINT,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY)
        )
        icon_label.pack(side=tk.LEFT, padx=(ModernStyle.PADDING_SM, 0))
        
        # Entry
        self.entry = tk.Entry(
            container,
            textvariable=textvariable,
            bg=ModernStyle.SURFACE,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_BODY),
            relief=tk.FLAT,
            borderwidth=0,
            **kwargs
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=ModernStyle.PADDING_SM, pady=ModernStyle.PADDING_SM)
        
        # Placeholder
        self.placeholder = placeholder
        self.textvariable = textvariable
        
        if not textvariable or not textvariable.get():
            self._show_placeholder()
        
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Hover effect
        container.bind("<Enter>", lambda e: container.configure(highlightbackground=ModernStyle.PRIMARY_LIGHT))
        container.bind("<Leave>", lambda e: container.configure(highlightbackground=ModernStyle.BORDER))
    
    def _show_placeholder(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=ModernStyle.TEXT_HINT)
    
    def _hide_placeholder(self):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=ModernStyle.TEXT_PRIMARY)
    
    def _on_focus_in(self, event):
        self._hide_placeholder()
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self._show_placeholder()


class GradientFrame(tk.Canvas):
    """
    Frame with gradient background.
    
    Note: Tkinter doesn't support native gradients,
    so we simulate with Canvas rectangles.
    """
    
    def __init__(
        self,
        parent,
        color1: str,
        color2: str,
        height: int = 200,
        **kwargs
    ):
        super().__init__(
            parent,
            height=height,
            highlightthickness=0,
            **kwargs
        )
        
        self.color1 = color1
        self.color2 = color2
        
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Draw gradient (simplified - single color for now)."""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # For simplicity, use solid color (Tkinter limitation)
        # In production, use PIL/Pillow for real gradients
        self.create_rectangle(
            0, 0, width, height,
            fill=self.color1,
            outline="",
            tags="gradient"
        )


class StatusBadge(tk.Label):
    """Colored status badge."""
    
    def __init__(
        self,
        parent,
        text: str,
        variant: str = "info",
        **kwargs
    ):
        colors = {
            "success": (ModernStyle.SUCCESS_LIGHT, ModernStyle.SUCCESS),
            "warning": ("#FEF3C7", ModernStyle.WARNING),
            "danger": (ModernStyle.DANGER_LIGHT, ModernStyle.DANGER),
            "info": (ModernStyle.PRIMARY_LIGHTER, ModernStyle.PRIMARY),
        }
        
        bg, fg = colors.get(variant, colors["info"])
        
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_SMALL, "bold"),
            padx=ModernStyle.PADDING_SM,
            pady=ModernStyle.PADDING_XS,
            **kwargs
        )


class IconButton(tk.Label):
    """
    Icon-only button (clickable label).
    
    Lighter than full button, good for actions in table rows.
    """
    
    def __init__(
        self,
        parent,
        icon: str,
        command=None,
        tooltip: str = "",
        fg: str = ModernStyle.TEXT_SECONDARY,
        hover_fg: str = ModernStyle.PRIMARY,
        **kwargs
    ):
        super().__init__(
            parent,
            text=icon,
            fg=fg,
            bg=ModernStyle.SURFACE,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_H3),
            cursor="hand2",
            **kwargs
        )
        
        if command:
            self.bind("<Button-1>", lambda e: command())
        
        # Hover effect
        self.bind("<Enter>", lambda e: self.configure(fg=hover_fg))
        self.bind("<Leave>", lambda e: self.configure(fg=fg))
