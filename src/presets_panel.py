"""
Quick Presets panel — one-click tweak bundles.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from tweak_manager import TweakManager


PRESETS = [
    {
        "name": "Gaming Mode",
        "description": (
            "Maximise frame rates and reduce input latency: disables background "
            "telemetry, enables Game Mode + Hardware-Accelerated GPU Scheduling, "
            "turns off mouse acceleration, and disables Xbox Game Bar."
        ),
        "icon": "🎮",
        "tweaks": {
            "game_mode": True,
            "game_hags": True,
            "game_no_mouse_accel": True,
            "game_disable_game_bar": True,
            "game_disable_xbox_dvr": True,
            "game_network_throttle": False,
            "perf_disable_telemetry": True,
            "sys_disable_background_apps": True,
            "power_high_performance": True,
        },
    },
    {
        "name": "Privacy Lock",
        "description": (
            "Aggressively cuts Microsoft data collection: disables Activity History, "
            "advertising ID, Cortana, location, telemetry, Start menu suggestions, "
            "and Windows Ink diagnostics."
        ),
        "icon": "🔒",
        "tweaks": {
            "privacy_activity_history": False,
            "privacy_advertising_id": False,
            "privacy_cortana": False,
            "privacy_location": False,
            "privacy_telemetry_level": 0,
            "privacy_start_suggestions": False,
            "privacy_inking_typing": False,
            "privacy_speech": False,
            "privacy_contacts": False,
            "privacy_clipboard_history": False,
        },
    },
    {
        "name": "Clean Desktop",
        "description": (
            "A minimal, clutter-free desktop: hides the Search icon, Task View, "
            "Widgets, and Chat buttons; shows file extensions; removes desktop icons "
            "and disables news & interests."
        ),
        "icon": "🖥️",
        "tweaks": {
            "taskbar_search": 0,
            "taskbar_task_view": False,
            "taskbar_widgets": False,
            "taskbar_chat": False,
            "explorer_file_extensions": True,
            "explorer_hidden_files": True,
            "taskbar_news": False,
        },
    },
    {
        "name": "Laptop Battery Saver",
        "description": (
            "Extends battery life: enables Power Saver plan, enables battery saver "
            "mode, turns off Bluetooth scanning, disables location, reduces screen "
            "timeout, and turns off background app refresh."
        ),
        "icon": "🔋",
        "tweaks": {
            "power_battery_saver": True,
            "power_sleep_timeout_battery": 5,
            "power_screen_timeout_battery": 3,
            "sys_disable_background_apps": True,
            "privacy_location": False,
            "net_disable_wifi_sense": True,
        },
    },
    {
        "name": "Dev Workstation",
        "description": (
            "Tuned for development: enables Developer Mode and long file paths, "
            "shows file extensions and hidden files, disables UAC prompts, enables "
            "Hyper-V, and turns on verbose startup/shutdown logging."
        ),
        "icon": "💻",
        "tweaks": {
            "dev_developer_mode": True,
            "dev_long_paths": True,
            "explorer_file_extensions": True,
            "explorer_hidden_files": True,
            "dev_verbose_startup": True,
            "dev_hyper_v": True,
        },
    },
]


class PresetCard(QWidget):
    def __init__(self, preset: dict, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.preset = preset
        self.manager = manager
        self._build()

    def _build(self):
        self.setStyleSheet(
            "PresetCard { background: #ffffff; border: 1px solid #d0d0d0; "
            "border-radius: 8px; }"
        )
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 16, 18, 16)
        outer.setSpacing(8)

        # Title row
        title_row = QHBoxLayout()
        icon = QLabel(self.preset["icon"])
        icon.setStyleSheet("font-size: 24px;")
        title_row.addWidget(icon)

        name = QLabel(self.preset["name"])
        f = QFont()
        f.setPointSize(12)
        f.setBold(True)
        name.setFont(f)
        title_row.addWidget(name)
        title_row.addStretch()
        outer.addLayout(title_row)

        # Description
        desc = QLabel(self.preset["description"])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #555555; font-size: 11px;")
        outer.addWidget(desc)

        # Tweak count
        count = QLabel(f"{len(self.preset['tweaks'])} tweaks included")
        count.setStyleSheet("color: #888888; font-size: 10px;")
        outer.addWidget(count)

        # Apply button
        btn = QPushButton("Apply Preset")
        btn.setFixedHeight(32)
        btn.setStyleSheet(
            "QPushButton { background: #0078d4; color: white; border: none; "
            "border-radius: 4px; font-size: 12px; }"
            "QPushButton:hover { background: #106ebe; }"
            "QPushButton:pressed { background: #005a9e; }"
        )
        btn.clicked.connect(self._apply)
        outer.addWidget(btn)

    def _apply(self):
        applied = 0
        skipped = []
        for tweak_id, value in self.preset["tweaks"].items():
            ok = self.manager.apply_tweak(tweak_id, value)
            if ok:
                applied += 1
            else:
                skipped.append(tweak_id)

        msg = f"Applied {applied} of {len(self.preset['tweaks'])} tweaks."
        if skipped:
            msg += f"\n\nSkipped (not found or failed):\n" + "\n".join(f"  • {t}" for t in skipped)
        QMessageBox.information(self, f"{self.preset['name']} — Done", msg)


class PresetsPanel(QWidget):
    def __init__(self, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        hdr = QLabel("Quick Presets")
        f = QFont()
        f.setPointSize(16)
        f.setBold(True)
        hdr.setFont(f)
        layout.addWidget(hdr)

        sub = QLabel(
            "One-click bundles that apply a curated set of tweaks for a specific use case. "
            "Each preset only touches the tweaks listed in its description — existing settings "
            "for other tweaks are left untouched."
        )
        sub.setWordWrap(True)
        sub.setStyleSheet("color: #666666; margin-bottom: 8px;")
        layout.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        for preset in PRESETS:
            card = PresetCard(preset, self.manager)
            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(container)
        main.addWidget(scroll)
