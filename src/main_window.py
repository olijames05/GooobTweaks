"""
Main application window for WinTweaks.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QStackedWidget,
    QLabel, QPushButton, QCheckBox, QComboBox, QSpinBox,
    QScrollArea, QMessageBox, QFrame, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from tweaks import TweakCategory, TWEAKS_BY_CATEGORY, ALL_TWEAKS, Tweak
from tweak_manager import TweakManager
from registry_utils import is_admin
from personalization_tab import PersonalizationTab
from presets_panel import PresetsPanel

_PRESETS_LABEL = "Quick Presets"

CATEGORY_DESCRIPTIONS = {
    TweakCategory.TASKBAR: "Customize the appearance and behavior of your taskbar.",
    TweakCategory.EXPLORER: "Modify File Explorer settings and appearance.",
    TweakCategory.SYSTEM: "Change system-wide settings and behaviors.",
    TweakCategory.NETWORK: "Tweak networking, IPv6, SMB and connectivity.",
    TweakCategory.POWER: "Power, battery, sleep and hibernation settings.",
    TweakCategory.GAMING: "Optimize Windows for gaming and competitive play.",
    TweakCategory.PRIVACY: "Control privacy settings and data collection.",
    TweakCategory.PERFORMANCE: "Optimize system performance.",
    TweakCategory.SECURITY: "Configure UAC, SmartScreen and Defender settings.",
    TweakCategory.APPS_SERVICES: "Disable bundled apps and unwanted services.",
    TweakCategory.CONTEXT_MENU: "Customize right-click context menus.",
    TweakCategory.PERSONALIZATION: "Customize visual appearance and effects.",
    TweakCategory.ACCESSIBILITY: "Tune mouse, keyboard and visual accessibility.",
    TweakCategory.DISPLAY: "Monitor resolution, scaling, refresh rate and colour settings.",
    TweakCategory.MOUSE_INPUT: "Mouse speed, pointer precision, touchpad and keyboard input.",
    TweakCategory.STARTUP_BOOT: "Control boot timeout, startup programs and fast-boot behaviour.",
    TweakCategory.NOTIFICATIONS: "Manage Action Centre, Focus Assist and per-app notifications.",
    TweakCategory.DEVELOPER: "Developer Mode, WSL, Hyper-V, long paths and sandbox settings.",
}


class TweakWidget(QWidget):
    """Widget for displaying and editing a single tweak."""

    _suppress_errors: bool = False  # class-level: "Dismiss All" sets this

    def __init__(self, tweak: Tweak, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.tweak = tweak
        self.manager = manager
        self._setup_ui()
        self._load_current_value()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        name_label = QLabel(self.tweak.name)
        name_font = QFont()
        name_font.setPointSize(11)
        name_font.setBold(True)
        name_label.setFont(name_font)
        layout.addWidget(name_label)

        desc_label = QLabel(self.tweak.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666666; margin-bottom: 5px;")
        layout.addWidget(desc_label)

        option = self.tweak.option

        if option.type == "checkbox":
            self.control = QCheckBox(option.label)
            self.control.setToolTip(option.description)
            self.control.stateChanged.connect(self._on_value_changed)
            layout.addWidget(self.control)

        elif option.type == "dropdown":
            control_layout = QHBoxLayout()
            label = QLabel(option.label + ":")
            control_layout.addWidget(label)
            self.control = QComboBox()
            for value, display in option.choices:
                self.control.addItem(display, value)
            self.control.setToolTip(option.description)
            self.control.currentIndexChanged.connect(self._on_value_changed)
            control_layout.addWidget(self.control, 1)
            layout.addLayout(control_layout)

        elif option.type == "spinbox":
            control_layout = QHBoxLayout()
            label = QLabel(option.label + ":")
            control_layout.addWidget(label)
            self.control = QSpinBox()
            if option.min_value is not None:
                self.control.setMinimum(option.min_value)
            if option.max_value is not None:
                self.control.setMaximum(option.max_value)
            self.control.setToolTip(option.description)
            self.control.valueChanged.connect(self._on_value_changed)
            control_layout.addWidget(self.control)
            control_layout.addStretch()
            layout.addLayout(control_layout)

        if self.tweak.requires_restart:
            warning = QLabel("⚠ Requires restart to take effect")
            warning.setStyleSheet("color: #d83b01; font-size: 11px;")
            layout.addWidget(warning)

        if self.tweak.requires_logoff:
            warning = QLabel("⚠ Requires sign out to take effect")
            warning.setStyleSheet("color: #d83b01; font-size: 11px;")
            layout.addWidget(warning)

        if self.tweak.requires_restart:
            restart_button = QPushButton("Restart Explorer")
            restart_button.setToolTip(
                "Restart File Explorer to apply this tweak immediately."
            )
            restart_button.clicked.connect(self._restart_explorer)
            layout.addWidget(restart_button)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(line)

        layout.addStretch()

    def _load_current_value(self):
        value = self.manager.get_tweak_value(self.tweak.id)
        # Block signals so setting the initial value doesn't fire _on_value_changed
        self.control.blockSignals(True)
        try:
            if self.tweak.option.type == "checkbox":
                self.control.setChecked(bool(value))
            elif self.tweak.option.type == "dropdown":
                index = self.control.findData(value)
                if index >= 0:
                    self.control.setCurrentIndex(index)
            elif self.tweak.option.type == "spinbox":
                try:
                    self.control.setValue(int(value) if value is not None else self.tweak.option.default)
                except (TypeError, ValueError):
                    self.control.setValue(self.tweak.option.default)
        finally:
            self.control.blockSignals(False)

    def _on_value_changed(self):
        if self.tweak.option.type == "checkbox":
            value = self.control.isChecked()
        elif self.tweak.option.type == "dropdown":
            value = self.control.currentData()
        elif self.tweak.option.type == "spinbox":
            value = self.control.value()
        else:
            return

        success = self.manager.apply_tweak(self.tweak.id, value)
        if not success:
            self._load_current_value()
            if TweakWidget._suppress_errors:
                return
            msg = QMessageBox(self)
            msg.setWindowTitle("Application Failed")
            msg.setText(
                f"Failed to apply '{self.tweak.name}'.\n\n"
                "Make sure you're running WinTweaks as Administrator."
            )
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
            dismiss_btn = msg.addButton("Dismiss All", QMessageBox.ButtonRole.RejectRole)
            msg.exec()
            if msg.clickedButton() == dismiss_btn:
                TweakWidget._suppress_errors = True

    def _restart_explorer(self):
        confirm = QMessageBox.question(
            self,
            "Restart Explorer",
            "Restart File Explorer now to apply this change?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            import subprocess
            subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"], capture_output=True)
            subprocess.Popen("explorer.exe")
            QMessageBox.information(self, "WinTweaks", "File Explorer has been restarted.")
        except Exception as exc:
            QMessageBox.warning(self, "WinTweaks", f"Could not restart File Explorer:\n{exc}")


class CategoryPage(QWidget):
    """Page showing all tweaks for a category."""

    def __init__(self, category: TweakCategory, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.category = category
        self.manager = manager
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel(self.category.value)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)

        desc = QLabel(CATEGORY_DESCRIPTIONS.get(self.category, ""))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; margin-bottom: 10px;")
        layout.addWidget(desc)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #cccccc;")
        layout.addWidget(line)

        tweaks = TWEAKS_BY_CATEGORY.get(self.category, [])
        for tweak in tweaks:
            tweak_widget = TweakWidget(tweak, self.manager)
            layout.addWidget(tweak_widget)

        layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)


class SearchResultsPage(QWidget):
    """Page showing search results across all tweaks."""

    def __init__(self, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self._results_layout = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._container = QWidget()
        self._results_layout = QVBoxLayout(self._container)
        self._results_layout.setContentsMargins(20, 20, 20, 20)
        self._results_layout.setSpacing(15)
        self._results_layout.addStretch()

        self._scroll.setWidget(self._container)
        main_layout.addWidget(self._scroll)

    def update_results(self, query: str):
        # Clear existing widgets
        while self._results_layout.count():
            item = self._results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        q = query.strip().lower()
        if not q:
            self._results_layout.addStretch()
            return

        header = QLabel(f'Search results for "{query}"')
        hf = QFont()
        hf.setPointSize(14)
        hf.setBold(True)
        header.setFont(hf)
        self._results_layout.addWidget(header)

        matches = [t for t in ALL_TWEAKS if q in t.name.lower() or q in t.description.lower()]

        if not matches:
            no_result = QLabel("No tweaks matched your search.")
            no_result.setStyleSheet("color: #888888;")
            self._results_layout.addWidget(no_result)
        else:
            count = QLabel(f"{len(matches)} tweak(s) found")
            count.setStyleSheet("color: #666666; font-size: 11px;")
            self._results_layout.addWidget(count)

            sep = QFrame()
            sep.setFrameShape(QFrame.Shape.HLine)
            sep.setStyleSheet("color: #cccccc;")
            self._results_layout.addWidget(sep)

            for tweak in matches:
                tw = TweakWidget(tweak, self.manager)
                self._results_layout.addWidget(tw)

        self._results_layout.addStretch()


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.manager = TweakManager()
        self._setup_ui()
        self._check_admin()

    def _setup_ui(self):
        self.setWindowTitle("WinTweaks")
        self.setMinimumSize(900, 600)
        self.resize(1100, 720)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #cccccc;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        sidebar_layout.setSpacing(0)

        title = QLabel("WinTweaks")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("padding: 10px 15px; color: #333333;")
        sidebar_layout.addWidget(title)

        version = QLabel("v2.5.0")
        version.setStyleSheet("padding: 0 15px 8px 15px; color: #888888; font-size: 11px;")
        sidebar_layout.addWidget(version)

        # Search bar
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search tweaks…")
        self._search.setStyleSheet(
            "QLineEdit { margin: 4px 10px 8px 10px; padding: 5px 8px; "
            "border: 1px solid #cccccc; border-radius: 4px; background: white; font-size: 12px; }"
            "QLineEdit:focus { border-color: #0078d4; }"
        )
        self._search.textChanged.connect(self._on_search_changed)
        sidebar_layout.addWidget(self._search)

        # Category list
        self.category_list = QListWidget()
        self.category_list.setFrameShape(QFrame.Shape.NoFrame)
        self.category_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 10px 15px;
                border: none;
                color: #333333;
                font-size: 12px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #e5e5e5;
            }
        """)

        # Quick Presets entry (sentinel value None)
        presets_item = QListWidgetItem(_PRESETS_LABEL)
        presets_item.setData(Qt.ItemDataRole.UserRole, None)
        self.category_list.addItem(presets_item)

        for category in TweakCategory:
            item = QListWidgetItem(category.value)
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.category_list.addItem(item)

        self.category_list.currentRowChanged.connect(self._on_category_changed)
        sidebar_layout.addWidget(self.category_list)

        self.admin_label = QLabel()
        self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px;")
        self.admin_label.setWordWrap(True)
        sidebar_layout.addWidget(self.admin_label)

        layout.addWidget(sidebar)

        # ── Content stack ────────────────────────────────────────────────────
        self.content_stack = QStackedWidget()

        # Search results page (index 0 in stack, but accessed by reference)
        self._search_page = SearchResultsPage(self.manager)
        self.content_stack.addWidget(self._search_page)

        # Quick Presets page
        self._presets_page = PresetsPanel(self.manager)
        self.content_stack.addWidget(self._presets_page)

        # Category pages
        self.category_pages = {}
        for category in TweakCategory:
            if category == TweakCategory.PERSONALIZATION:
                page = PersonalizationTab()
            else:
                page = CategoryPage(category, self.manager)
            self.category_pages[category] = page
            self.content_stack.addWidget(page)

        layout.addWidget(self.content_stack, 1)

        # Start on Quick Presets (row 0)
        self.category_list.setCurrentRow(0)

    def _on_search_changed(self, text: str):
        if text.strip():
            self._search_page.update_results(text)
            self.content_stack.setCurrentWidget(self._search_page)
            # Deselect category list while searching
            self.category_list.clearSelection()
        else:
            # Restore previously selected category page
            row = self.category_list.currentRow()
            if row >= 0:
                self._on_category_changed(row)

    def _on_category_changed(self, index):
        # If a search is active, ignore category clicks
        if self._search.text().strip():
            return
        item = self.category_list.item(index)
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole)
        if data is None:
            # Quick Presets
            self.content_stack.setCurrentWidget(self._presets_page)
        else:
            page = self.category_pages.get(data)
            if page:
                self.content_stack.setCurrentWidget(page)

    def _check_admin(self):
        if is_admin():
            self.admin_label.setText("✓ Running as Administrator")
            self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px; color: #107c10;")
        else:
            self.admin_label.setText("⚠ Not running as Administrator\nSome tweaks may not work")
            self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px; color: #d83b01;")
