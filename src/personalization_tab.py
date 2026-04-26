"""
Personalization hub for WinTweaks.

This page groups the main appearance tools into separate tabs so the feature set
can grow without turning into a monolithic widget.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from custom_features_beta_panel import CustomFeaturesBetaPanel
from wallpaper_icons_panel import WallpaperAndIconsPanel


class PersonalizationTab(QWidget):
    """Main personalization page containing all appearance-related tools."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header = QLabel("Personalization")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        layout.addWidget(header)

        description = QLabel(
            "Customize wallpapers, icons, and experimental registry-based features."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        layout.addWidget(description)

        self.tabs = QTabWidget()
        self.tabs.addTab(WallpaperAndIconsPanel(), "Wallpaper & Icons")
        self.tabs.addTab(CustomFeaturesBetaPanel(), "Custom Features (Beta)")

        layout.addWidget(self.tabs, 1)
