"""Modern Glassmorphism Design System."""

from __future__ import annotations


class ModernStyle:
    """
    Modern Glassmorphism Design System.
    
    Inspired by:
    - Apple's iOS design language
    - Windows 11 Fluent Design
    - Modern web design trends (2024-2026)
    """
    
    # ===== GLASSMORPHISM COLOR PALETTE =====
    
    # Primary Colors (Purple-Blue Gradient)
    PRIMARY = "#6366F1"  # Indigo-500
    PRIMARY_DARK = "#4F46E5"  # Indigo-600
    PRIMARY_LIGHT = "#A5B4FC"  # Indigo-300
    PRIMARY_LIGHTER = "#C7D2FE"  # Indigo-200
    
    # Accent Colors
    ACCENT = "#EC4899"  # Pink-500
    ACCENT_LIGHT = "#F9A8D4"  # Pink-300
    
    # Semantic Colors
    SUCCESS = "#10B981"  # Emerald-500
    SUCCESS_LIGHT = "#6EE7B7"  # Emerald-300
    WARNING = "#F59E0B"  # Amber-500
    DANGER = "#EF4444"  # Red-500
    DANGER_LIGHT = "#FCA5A5"  # Red-300
    
    # Neutral Colors (Light Theme)
    WHITE = "#FFFFFF"
    BACKGROUND = "#F8FAFC"  # Slate-50
    BACKGROUND_DARK = "#F1F5F9"  # Slate-100
    SURFACE = "#FFFFFF"
    SURFACE_HOVER = "#F8FAFC"
    
    # Glass Effect Colors
    GLASS_BG = "#FFFFFF"  # Semi-transparent white
    GLASS_BORDER = "#E2E8F0"  # Slate-200
    GLASS_SHADOW = "#94A3B8"  # Slate-400
    
    # Text Colors (Better contrast)
    TEXT_PRIMARY = "#0F172A"  # Slate-900 - Darker for better readability
    TEXT_SECONDARY = "#475569"  # Slate-600 - Darker
    TEXT_HINT = "#94A3B8"  # Slate-400
    TEXT_ON_PRIMARY = "#FFFFFF"
    TEXT_ON_SUCCESS = "#FFFFFF"
    
    # Border & Shadow
    BORDER = "#E2E8F0"  # Slate-200
    BORDER_LIGHT = "#F1F5F9"  # Slate-100
    SHADOW_COLOR = "rgba(148, 163, 184, 0.2)"  # Slate-400 with opacity
    
    # ===== TYPOGRAPHY =====
    
    FONT_FAMILY = "Segoe UI"  # Windows
    FONT_FAMILY_ALT = "SF Pro Display"  # macOS fallback
    
    FONT_SIZE_H1 = 28
    FONT_SIZE_H2 = 20
    FONT_SIZE_H3 = 16
    FONT_SIZE_BODY = 11
    FONT_SIZE_TABLE = 11
    FONT_SIZE_SMALL = 10
    FONT_SIZE_TINY = 9
    
    FONT_WEIGHT_BOLD = "bold"
    FONT_WEIGHT_NORMAL = "normal"
    
    # ===== LAYOUT & SPACING =====
    
    # Spacing Scale (8px base)
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 12
    SPACE_LG = 16
    SPACE_XL = 24
    SPACE_2XL = 32
    SPACE_3XL = 48
    
    # Padding
    PADDING_XS = 4
    PADDING_SM = 8
    PADDING_MD = 12
    PADDING_LG = 16
    PADDING_XL = 24
    
    # Border Radius (Rounded Corners)
    RADIUS_SM = 6
    RADIUS_MD = 10
    RADIUS_LG = 14
    RADIUS_XL = 20
    RADIUS_FULL = 999
    
    # Table
    TABLE_ROW_HEIGHT = 48
    TABLE_HEADER_HEIGHT = 44
    
    # Button Heights
    BUTTON_HEIGHT_SM = 32
    BUTTON_HEIGHT_MD = 40
    BUTTON_HEIGHT_LG = 48
    
    # ===== EFFECTS =====
    
    # Shadows (simulate with borders)
    SHADOW_SM = "1px solid #F1F5F9"
    SHADOW_MD = "2px solid #E2E8F0"
    SHADOW_LG = "3px solid #CBD5E1"
    
    # Hover Effects
    HOVER_OPACITY = 0.9
    ACTIVE_OPACITY = 0.85
    
    # Transition Duration (ms)
    TRANSITION_FAST = 150
    TRANSITION_NORMAL = 250
    TRANSITION_SLOW = 350


class GradientColors:
    """Gradient color combinations."""
    
    # Primary Gradient (Purple to Blue)
    PRIMARY_START = "#6366F1"  # Indigo
    PRIMARY_END = "#8B5CF6"  # Violet
    
    # Accent Gradient (Pink to Orange)
    ACCENT_START = "#EC4899"  # Pink
    ACCENT_END = "#F97316"  # Orange
    
    # Success Gradient (Green to Teal)
    SUCCESS_START = "#10B981"  # Emerald
    SUCCESS_END = "#14B8A6"  # Teal
    
    # Background Gradient (Light)
    BG_START = "#F8FAFC"  # Slate-50
    BG_END = "#EFF6FF"  # Blue-50


class Icons:
    """Unicode icons for modern UI."""
    
    # Actions
    ADD = "＋"
    EDIT = "✎"
    DELETE = "🗑"
    REFRESH = "⟳"
    SEARCH = "🔍"
    CLOSE = "✕"
    CHECK = "✓"
    
    # Navigation
    ARROW_LEFT = "←"
    ARROW_RIGHT = "→"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"
    
    # Status
    SUCCESS = "✓"
    ERROR = "✕"
    WARNING = "⚠"
    INFO = "ⓘ"
    
    # Content
    DASHBOARD = "📊"
    CHART = "📈"
    LIST = "📋"
    SETTINGS = "⚙"
    USER = "👤"
