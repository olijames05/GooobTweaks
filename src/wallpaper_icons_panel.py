"""
Wallpaper and desktop icon controls for WinTweaks.
"""

from __future__ import annotations

import os
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QColorDialog,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from icon_manager import IconManager
from wallpaper_manager import WallpaperManager


class WallpaperAndIconsPanel(QWidget):
    """Combined controls for wallpaper and desktop icon customization."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.wallpaper_manager = WallpaperManager()
        self.icon_manager = IconManager()
        self.current_wallpaper_path = self.wallpaper_manager.get_current_wallpaper()
        self._setup_ui()
        self._refresh_status()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        layout.addWidget(self._build_wallpaper_group())
        layout.addWidget(self._build_desktop_icons_group())

    def _build_wallpaper_group(self) -> QGroupBox:
        group = QGroupBox("Wallpaper")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        self.wallpaper_path_label = QLabel()
        self.wallpaper_path_label.setWordWrap(True)
        self.wallpaper_path_label.setStyleSheet("color: #444444;")
        layout.addWidget(self.wallpaper_path_label)

        buttons_row = QHBoxLayout()

        choose_button = QPushButton("Choose Image")
        choose_button.clicked.connect(self._choose_wallpaper)
        buttons_row.addWidget(choose_button)

        color_button = QPushButton("Set Solid Color")
        color_button.clicked.connect(self._choose_solid_color)
        buttons_row.addWidget(color_button)

        buttons_row.addStretch()
        layout.addLayout(buttons_row)

        style_row = QHBoxLayout()
        style_row.setSpacing(8)

        for style_name in ("fill", "fit", "stretch", "tile", "center"):
            style_button = QPushButton(style_name.title())
            style_button.clicked.connect(lambda checked=False, value=style_name: self._apply_wallpaper_style(value))
            style_row.addWidget(style_button)

        style_row.addStretch()
        layout.addLayout(style_row)

        hint = QLabel("Tip: choose an image first, then pick a display mode.")
        hint.setStyleSheet("color: #777777; font-size: 11px;")
        layout.addWidget(hint)

        return group

    def _build_desktop_icons_group(self) -> QGroupBox:
        group = QGroupBox("Desktop Icons")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        description = QLabel(
            "Show or hide standard desktop icons for the current user."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        layout.addWidget(description)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        self.icon_buttons = {}
        icon_items = [
            ("computer", "This PC"),
            ("recycle_bin", "Recycle Bin"),
            ("user_files", "User Files"),
            ("network", "Network"),
            ("control_panel", "Control Panel"),
        ]

        for row, (icon_key, label_text) in enumerate(icon_items):
            label = QLabel(label_text)
            show_button = QPushButton("Show")
            hide_button = QPushButton("Hide")

            show_button.clicked.connect(
                lambda checked=False, key=icon_key: self._toggle_desktop_icon(key, True)
            )
            hide_button.clicked.connect(
                lambda checked=False, key=icon_key: self._toggle_desktop_icon(key, False)
            )

            grid.addWidget(label, row, 0)
            grid.addWidget(show_button, row, 1)
            grid.addWidget(hide_button, row, 2)

            self.icon_buttons[icon_key] = (show_button, hide_button)

        layout.addLayout(grid)

        refresh_row = QHBoxLayout()
        refresh_button = QPushButton("Refresh Status")
        refresh_button.clicked.connect(self._refresh_status)
        refresh_row.addWidget(refresh_button)
        refresh_row.addStretch()
        layout.addLayout(refresh_row)

        return group

    def _choose_wallpaper(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Wallpaper",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*)",
        )
        if not file_path:
            return

        self.current_wallpaper_path = file_path
        self._apply_wallpaper_style("fill")

    def _choose_solid_color(self) -> None:
        color = QColorDialog.getColor(QColor("#2b2b2b"), self, "Choose Background Color")
        if not color.isValid():
            return

        success = self.wallpaper_manager.set_solid_color(color.name())
        if success:
            self.current_wallpaper_path = None
            self._show_message("Success", "Solid background color applied.")
            self._refresh_status()
        else:
            self._show_error("Failed to apply the solid background color.")

    def _apply_wallpaper_style(self, style: str) -> None:
        if not self.current_wallpaper_path:
            current = self.wallpaper_manager.get_current_wallpaper()
            if current and os.path.exists(current):
                self.current_wallpaper_path = current
            else:
                self._show_error("Choose an image first.")
                return

        success = self.wallpaper_manager.set_static_wallpaper(self.current_wallpaper_path, style)
        if success:
            self._show_message("Success", f"Wallpaper applied using '{style}' style.")
            self._refresh_status()
        else:
            self._show_error("Failed to apply the wallpaper.")

    def _toggle_desktop_icon(self, icon_type: str, show: bool) -> None:
        success = self.icon_manager.show_desktop_icon(icon_type, show)
        if success:
            action = "Shown" if show else "Hidden"
            label = icon_type.replace("_", " ").title()
            self._show_message("Success", f"{action} {label}.")
            self._refresh_status()
        else:
            self._show_error(f"Failed to {'show' if show else 'hide'} {icon_type.replace('_', ' ')}.")

    def _refresh_status(self) -> None:
        wallpaper_path = self.current_wallpaper_path or self.wallpaper_manager.get_current_wallpaper()
        if wallpaper_path:
            display_text = wallpaper_path
        else:
            display_text = "No wallpaper image selected"

        self.wallpaper_path_label.setText(f"Current wallpaper: {display_text}")

    def _show_message(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "WinTweaks", message)
