"""
Main application window for WinTweaks.
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QStackedWidget,
    QLabel, QPushButton, QCheckBox, QComboBox, QSpinBox,
    QGroupBox, QScrollArea, QMessageBox, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from tweaks import TweakCategory, TWEAKS_BY_CATEGORY, ALL_TWEAKS, Tweak
from tweak_manager import TweakManager
from registry_utils import is_admin
from personalization_tab import PersonalizationTab


class TweakWidget(QWidget):
    """Widget for displaying and editing a single tweak."""
    
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
        
        # Header with name
        name_label = QLabel(self.tweak.name)
        name_font = QFont()
        name_font.setPointSize(11)
        name_font.setBold(True)
        name_label.setFont(name_font)
        layout.addWidget(name_label)
        
        # Description
        desc_label = QLabel(self.tweak.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666666; margin-bottom: 5px;")
        layout.addWidget(desc_label)
        
        # Control based on option type
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
        
        # Warning labels
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
        
        # Add separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(line)
        
        layout.addStretch()
    
    def _load_current_value(self):
        """Load the current value from the registry."""
        value = self.manager.get_tweak_value(self.tweak.id)
        
        if self.tweak.option.type == "checkbox":
            self.control.setChecked(bool(value))
        elif self.tweak.option.type == "dropdown":
            index = self.control.findData(value)
            if index >= 0:
                self.control.setCurrentIndex(index)
        elif self.tweak.option.type == "spinbox":
            self.control.setValue(int(value) if value else self.tweak.option.default)
    
    def _on_value_changed(self):
        """Handle value change and apply the tweak."""
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
            # Revert the control if application failed
            self._load_current_value()
            QMessageBox.warning(
                self,
                "Application Failed",
                f"Failed to apply '{self.tweak.name}'.\n\n"
                "Make sure you're running WinTweaks as Administrator."
            )
    
    def _restart_explorer(self):
        """Restart File Explorer so restart-required tweaks take effect immediately."""
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

            subprocess.run(
                ["taskkill", "/F", "/IM", "explorer.exe"],
                capture_output=True,
            )
            subprocess.Popen("explorer.exe")
            QMessageBox.information(
                self,
                "WinTweaks",
                "File Explorer has been restarted.",
            )
        except Exception as exc:
            QMessageBox.warning(
                self,
                "WinTweaks",
                f"Could not restart File Explorer:\n{exc}",
            )


class CategoryPage(QWidget):
    """Page showing all tweaks for a category."""
    
    def __init__(self, category: TweakCategory, manager: TweakManager, parent=None):
        super().__init__(parent)
        self.category = category
        self.manager = manager
        self._setup_ui()
    
    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container widget for scroll area
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Category header
        header = QLabel(self.category.value)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Description based on category
        descriptions = {
            TweakCategory.TASKBAR: "Customize the appearance and behavior of your taskbar.",
            TweakCategory.EXPLORER: "Modify File Explorer settings and appearance.",
            TweakCategory.SYSTEM: "Change system-wide settings and behaviors.",
            TweakCategory.PRIVACY: "Control privacy settings and data collection.",
            TweakCategory.PERFORMANCE: "Optimize system performance.",
            TweakCategory.CONTEXT_MENU: "Customize right-click context menus.",
            TweakCategory.PERSONALIZATION: "Customize visual appearance and effects.",
        }
        
        desc = QLabel(descriptions.get(self.category, ""))
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #cccccc;")
        layout.addWidget(line)
        
        # Add tweak widgets
        tweaks = TWEAKS_BY_CATEGORY.get(self.category, [])
        for tweak in tweaks:
            tweak_widget = TweakWidget(tweak, self.manager)
            layout.addWidget(tweak_widget)
        
        layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)


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
        self.resize(1000, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #cccccc;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        sidebar_layout.setSpacing(0)
        
        # App title in sidebar
        title = QLabel("WinTweaks")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("padding: 10px 15px; color: #333333;")
        sidebar_layout.addWidget(title)
        
        version = QLabel("v1.5.0")
        version.setStyleSheet("padding: 0 15px 15px 15px; color: #888888; font-size: 11px;")
        sidebar_layout.addWidget(version)
        
        # Category list
        self.category_list = QListWidget()
        self.category_list.setFrameShape(QFrame.Shape.NoFrame)
        self.category_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 12px 15px;
                border: none;
                color: #333333;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #e5e5e5;
            }
        """)
        
        # Add categories
        for category in TweakCategory:
            item = QListWidgetItem(category.value)
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.category_list.addItem(item)
        
        self.category_list.currentRowChanged.connect(self._on_category_changed)
        sidebar_layout.addWidget(self.category_list)
        
        # Admin status label
        self.admin_label = QLabel()
        self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px;")
        self.admin_label.setWordWrap(True)
        sidebar_layout.addWidget(self.admin_label)
        
        layout.addWidget(sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        
        # Create pages for each category
        self.category_pages = {}
        for category in TweakCategory:
            if category == TweakCategory.PERSONALIZATION:
                # Use special personalization tab with wallpaper/fonts
                page = PersonalizationTab()
            else:
                page = CategoryPage(category, self.manager)
            self.category_pages[category] = page
            self.content_stack.addWidget(page)
        
        layout.addWidget(self.content_stack, 1)
        
        # Select first category
        self.category_list.setCurrentRow(0)
    
    def _on_category_changed(self, index):
        """Handle category selection change."""
        item = self.category_list.item(index)
        if item:
            category = item.data(Qt.ItemDataRole.UserRole)
            page = self.category_pages.get(category)
            if page:
                self.content_stack.setCurrentWidget(page)
    
    def _check_admin(self):
        """Check if running as admin and update UI accordingly."""
        if is_admin():
            self.admin_label.setText("✓ Running as Administrator")
            self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px; color: #107c10;")
        else:
            self.admin_label.setText("⚠ Not running as Administrator\nSome tweaks may not work")
            self.admin_label.setStyleSheet("padding: 10px 15px; font-size: 11px; color: #d83b01;")
