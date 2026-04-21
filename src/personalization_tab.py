"""
Personalization tab with wallpaper, video wallpaper, themes, and icon customization.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QComboBox, QSpinBox, QGroupBox, QGridLayout,
    QLineEdit, QColorDialog, QMessageBox, QListWidget,
    QListWidgetItem, QProgressBar, QCheckBox, QSlider,
    QTabWidget, QScrollArea, QFrame, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QIcon

from wallpaper_manager import WallpaperManager
from video_wallpaper import VideoWallpaperManager
from font_manager import FontManager
from theme_manager import ThemeManager
from icon_manager import IconManager


class WallpaperWidget(QWidget):
    """Widget for wallpaper customization including video wallpapers."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallpaper_manager = WallpaperManager()
        self.video_manager = VideoWallpaperManager()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_animation_status)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Static Wallpaper Section
        static_group = QGroupBox("Static Wallpaper (Works on Unactivated Windows)")
        static_layout = QVBoxLayout(static_group)
        
        # Current wallpaper display
        current_layout = QHBoxLayout()
        current_layout.addWidget(QLabel("Current Wallpaper:"))
        self.current_wallpaper_label = QLabel("Loading...")
        self.current_wallpaper_label.setWordWrap(True)
        current_layout.addWidget(self.current_wallpaper_label, 1)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_current_wallpaper)
        current_layout.addWidget(refresh_btn)
        static_layout.addLayout(current_layout)
        
        # Wallpaper style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Wallpaper Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Fill", "Fit", "Stretch", "Tile", "Center", "Span"])
        self.style_combo.setCurrentText("Fill")
        style_layout.addWidget(self.style_combo)
        style_layout.addStretch()
        static_layout.addLayout(style_layout)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select an image file...")
        file_layout.addWidget(self.file_path)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_wallpaper)
        file_layout.addWidget(browse_btn)
        
        apply_btn = QPushButton("Apply Wallpaper")
        apply_btn.clicked.connect(self._apply_wallpaper)
        file_layout.addWidget(apply_btn)
        static_layout.addLayout(file_layout)
        
        # Solid color option
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Or set solid color:"))
        self.color_preview = QLabel("    ")
        self.color_preview.setStyleSheet("background-color: #0078d4; border: 1px solid #ccc;")
        self.color_preview.setFixedSize(30, 30)
        color_layout.addWidget(self.color_preview)
        
        self.selected_color = "#0078d4"
        color_btn = QPushButton("Choose Color...")
        color_btn.clicked.connect(self._choose_color)
        color_layout.addWidget(color_btn)
        
        apply_color_btn = QPushButton("Apply Color")
        apply_color_btn.clicked.connect(self._apply_color)
        color_layout.addWidget(apply_color_btn)
        color_layout.addStretch()
        static_layout.addLayout(color_layout)
        
        layout.addWidget(static_group)
        
        # Video Wallpaper Section
        video_group = QGroupBox("Video Wallpaper (MP4, WebM, AVI)")
        video_layout = QVBoxLayout(video_group)
        
        video_info = QLabel("Play video files as your desktop wallpaper. Requires VLC, MPV, or FFmpeg.")
        video_info.setWordWrap(True)
        video_info.setStyleSheet("color: #666; font-size: 11px;")
        video_layout.addWidget(video_info)
        
        # Video file selection
        video_file_layout = QHBoxLayout()
        video_file_layout.addWidget(QLabel("Video File:"))
        self.video_path = QLineEdit()
        self.video_path.setPlaceholderText("Select a video file...")
        video_file_layout.addWidget(self.video_path)
        
        browse_video_btn = QPushButton("Browse...")
        browse_video_btn.clicked.connect(self._browse_video)
        video_file_layout.addWidget(browse_video_btn)
        video_layout.addLayout(video_file_layout)
        
        # Video options
        video_options = QHBoxLayout()
        self.video_audio = QCheckBox("Enable Audio")
        self.video_audio.setToolTip("Play video audio (not recommended)")
        video_options.addWidget(self.video_audio)
        
        video_options.addWidget(QLabel("Speed:"))
        self.video_speed = QComboBox()
        self.video_speed.addItems(["0.5x", "1.0x", "1.5x", "2.0x"])
        self.video_speed.setCurrentText("1.0x")
        video_options.addWidget(self.video_speed)
        video_options.addStretch()
        video_layout.addLayout(video_options)
        
        # Video controls
        video_controls = QHBoxLayout()
        self.start_video_btn = QPushButton("Start Video Wallpaper")
        self.start_video_btn.clicked.connect(self._start_video_wallpaper)
        self.start_video_btn.setStyleSheet("background-color: #107c10;")
        video_controls.addWidget(self.start_video_btn)
        
        self.stop_video_btn = QPushButton("Stop Video")
        self.stop_video_btn.clicked.connect(self._stop_video_wallpaper)
        self.stop_video_btn.setEnabled(False)
        video_controls.addWidget(self.stop_video_btn)
        
        self.video_status = QLabel("Status: Stopped")
        video_controls.addWidget(self.video_status)
        video_controls.addStretch()
        video_layout.addLayout(video_controls)
        
        layout.addWidget(video_group)
        
        # Animated Wallpaper Section
        anim_group = QGroupBox("Animated Wallpaper (Image Slideshow)")
        anim_layout = QVBoxLayout(anim_group)
        
        # Folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Image Folder:"))
        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("Select a folder with images...")
        folder_layout.addWidget(self.folder_path)
        
        browse_folder_btn = QPushButton("Browse...")
        browse_folder_btn.clicked.connect(self._browse_folder)
        folder_layout.addWidget(browse_folder_btn)
        anim_layout.addLayout(folder_layout)
        
        # Interval setting
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Change Interval:"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3600)
        self.interval_spin.setValue(30)
        self.interval_spin.setSuffix(" seconds")
        interval_layout.addWidget(self.interval_spin)
        interval_layout.addStretch()
        anim_layout.addLayout(interval_layout)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.start_anim_btn = QPushButton("Start Animation")
        self.start_anim_btn.clicked.connect(self._start_animation)
        control_layout.addWidget(self.start_anim_btn)
        
        self.stop_anim_btn = QPushButton("Stop Animation")
        self.stop_anim_btn.clicked.connect(self._stop_animation)
        self.stop_anim_btn.setEnabled(False)
        control_layout.addWidget(self.stop_anim_btn)
        
        self.anim_status = QLabel("Status: Stopped")
        control_layout.addWidget(self.anim_status)
        control_layout.addStretch()
        anim_layout.addLayout(control_layout)
        
        layout.addWidget(anim_group)
        
        # Quick Actions
        quick_group = QGroupBox("Quick Actions")
        quick_layout = QHBoxLayout(quick_group)
        
        spotlight_btn = QPushButton("Use Windows Spotlight")
        spotlight_btn.clicked.connect(self._use_spotlight)
        spotlight_btn.setToolTip("Use Windows Spotlight images as wallpaper")
        quick_layout.addWidget(spotlight_btn)
        
        default_btn = QPushButton("Reset to Default")
        default_btn.clicked.connect(self._reset_default)
        quick_layout.addWidget(default_btn)
        
        quick_layout.addStretch()
        layout.addWidget(quick_group)
        
        layout.addStretch()
        
        # Load current wallpaper
        self._refresh_current_wallpaper()
        self.animation_timer.start(1000)
    
    def _refresh_current_wallpaper(self):
        """Refresh the current wallpaper display."""
        current = self.wallpaper_manager.get_current_wallpaper()
        if current:
            self.current_wallpaper_label.setText(current)
        else:
            self.current_wallpaper_label.setText("(Solid color or default wallpaper)")
    
    def _browse_wallpaper(self):
        """Browse for a wallpaper image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wallpaper",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if file_path:
            self.file_path.setText(file_path)
    
    def _apply_wallpaper(self):
        """Apply the selected wallpaper."""
        file_path = self.file_path.text()
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", "Please select a valid image file.")
            return
        
        style = self.style_combo.currentText().lower()
        
        if self.wallpaper_manager.set_static_wallpaper(file_path, style):
            QMessageBox.information(self, "Success", "Wallpaper applied successfully!")
            self._refresh_current_wallpaper()
        else:
            QMessageBox.critical(self, "Error", "Failed to apply wallpaper.")
    
    def _choose_color(self):
        """Open color picker dialog."""
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self.color_preview.setStyleSheet(f"background-color: {self.selected_color}; border: 1px solid #ccc;")
    
    def _apply_color(self):
        """Apply solid color wallpaper."""
        if self.wallpaper_manager.set_solid_color(self.selected_color):
            QMessageBox.information(self, "Success", "Solid color applied!")
            self._refresh_current_wallpaper()
        else:
            QMessageBox.critical(self, "Error", "Failed to apply color.")
    
    def _browse_video(self):
        """Browse for video file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Videos (*.mp4 *.webm *.avi *.mov *.mkv)"
        )
        if file_path:
            self.video_path.setText(file_path)
    
    def _start_video_wallpaper(self):
        """Start video wallpaper."""
        video_path = self.video_path.text()
        if not video_path or not os.path.exists(video_path):
            QMessageBox.warning(self, "Error", "Please select a valid video file.")
            return
        
        speed_text = self.video_speed.currentText().replace("x", "")
        speed = float(speed_text)
        audio = self.video_audio.isChecked()
        
        if self.video_manager.set_video_wallpaper(video_path, audio, speed):
            self.start_video_btn.setEnabled(False)
            self.stop_video_btn.setEnabled(True)
            self.video_status.setText("Status: Playing")
            self.video_status.setStyleSheet("color: #107c10;")
        else:
            QMessageBox.critical(
                self, 
                "Error", 
                "Failed to start video wallpaper.\n\n"
                "Please install VLC, MPV, or FFmpeg to use this feature."
            )
    
    def _stop_video_wallpaper(self):
        """Stop video wallpaper."""
        self.video_manager.stop_video_wallpaper()
        self.start_video_btn.setEnabled(True)
        self.stop_video_btn.setEnabled(False)
        self.video_status.setText("Status: Stopped")
        self.video_status.setStyleSheet("")
    
    def _browse_folder(self):
        """Browse for image folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.folder_path.setText(folder)
    
    def _start_animation(self):
        """Start animated wallpaper."""
        folder = self.folder_path.text()
        if not folder or not os.path.exists(folder):
            QMessageBox.warning(self, "Error", "Please select a valid folder.")
            return
        
        images = []
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                images.append(os.path.join(folder, file))
        
        if not images:
            QMessageBox.warning(self, "Error", "No images found in the selected folder.")
            return
        
        interval = self.interval_spin.value()
        
        if self.wallpaper_manager.start_animated_wallpaper(images, interval):
            self.start_anim_btn.setEnabled(False)
            self.stop_anim_btn.setEnabled(True)
            self.anim_status.setText("Status: Running")
        else:
            QMessageBox.critical(self, "Error", "Failed to start animation.")
    
    def _stop_animation(self):
        """Stop animated wallpaper."""
        self.wallpaper_manager.stop_animated_wallpaper()
        self.start_anim_btn.setEnabled(True)
        self.stop_anim_btn.setEnabled(False)
        self.anim_status.setText("Status: Stopped")
    
    def _update_animation_status(self):
        """Update animation status label."""
        if self.wallpaper_manager.is_animation_running():
            self.anim_status.setText("Status: Running")
        else:
            if not self.start_anim_btn.isEnabled():
                self.start_anim_btn.setEnabled(True)
                self.stop_anim_btn.setEnabled(False)
                self.anim_status.setText("Status: Stopped")
        
        # Update video status
        if self.video_manager.is_playing():
            self.video_status.setText("Status: Playing")
            self.video_status.setStyleSheet("color: #107c10;")
        elif not self.start_video_btn.isEnabled():
            self.start_video_btn.setEnabled(True)
            self.stop_video_btn.setEnabled(False)
            self.video_status.setText("Status: Stopped")
            self.video_status.setStyleSheet("")
    
    def _use_spotlight(self):
        """Use Windows Spotlight images."""
        images = self.wallpaper_manager.get_spotlight_images()
        if images:
            self.wallpaper_manager.start_animated_wallpaper(images, 300)
            QMessageBox.information(self, "Success", "Windows Spotlight wallpaper started!")
        else:
            QMessageBox.warning(self, "Error", "No Windows Spotlight images found.")
    
    def _reset_default(self):
        """Reset to default Windows wallpaper."""
        default_path = os.path.expandvars(r"%SystemRoot%\Web\Wallpaper\Windows\img0.jpg")
        if os.path.exists(default_path):
            self.wallpaper_manager.set_static_wallpaper(default_path, "fill")
            QMessageBox.information(self, "Success", "Reset to default wallpaper!")
            self._refresh_current_wallpaper()
        else:
            QMessageBox.warning(self, "Error", "Default wallpaper not found.")


class ThemesWidget(QWidget):
    """Widget for theme customization."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Preset Themes
        preset_group = QGroupBox("Preset Color Themes")
        preset_layout = QGridLayout(preset_group)
        
        themes = self.theme_manager.get_available_themes()
        row, col = 0, 0
        
        for theme_id, theme_name in themes.items():
            if theme_id == "default":
                continue
                
            btn = QPushButton(theme_name)
            btn.setMinimumHeight(50)
            
            # Set button color based on theme
            theme_colors = {
                "orange": "#FF6B35",
                "blue": "#0066CC",
                "violet": "#7B2CBF",
                "green": "#2D6A4F",
                "red": "#C9184A",
                "pink": "#FF006E",
                "cyan": "#00B4D8",
                "yellow": "#FFB703",
                "purple": "#7209B7",
                "teal": "#0A9396",
                "black": "#333333",
            }
            
            color = theme_colors.get(theme_id, "#0078D4")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    opacity: 0.8;
                }}
            """)
            
            btn.clicked.connect(lambda checked, tid=theme_id: self._apply_theme(tid))
            preset_layout.addWidget(btn, row, col)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addWidget(preset_group)
        
        # Custom Theme
        custom_group = QGroupBox("Custom Theme")
        custom_layout = QGridLayout(custom_group)
        
        # Accent color
        custom_layout.addWidget(QLabel("Accent Color:"), 0, 0)
        self.accent_preview = QLabel("    ")
        self.accent_preview.setFixedSize(40, 40)
        self.accent_preview.setStyleSheet("background-color: #FF5733; border: 2px solid #ccc; border-radius: 4px;")
        custom_layout.addWidget(self.accent_preview, 0, 1)
        
        self.custom_color = "#FF5733"
        color_btn = QPushButton("Choose Color...")
        color_btn.clicked.connect(self._choose_custom_color)
        custom_layout.addWidget(color_btn, 0, 2)
        
        # Dark mode
        custom_layout.addWidget(QLabel("Mode:"), 1, 0)
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.dark_mode_check.setChecked(True)
        custom_layout.addWidget(self.dark_mode_check, 1, 1)
        
        # Transparency
        self.transparency_check = QCheckBox("Transparency Effects")
        self.transparency_check.setChecked(True)
        custom_layout.addWidget(self.transparency_check, 1, 2)
        
        # Colorize options
        self.colorize_taskbar = QCheckBox("Colorize Taskbar")
        self.colorize_taskbar.setChecked(True)
        custom_layout.addWidget(self.colorize_taskbar, 2, 1)
        
        self.colorize_start = QCheckBox("Colorize Start Menu")
        self.colorize_start.setChecked(True)
        custom_layout.addWidget(self.colorize_start, 2, 2)
        
        # Apply button
        apply_custom_btn = QPushButton("Apply Custom Theme")
        apply_custom_btn.clicked.connect(self._apply_custom_theme)
        apply_custom_btn.setStyleSheet("background-color: #0078d4; font-weight: bold;")
        custom_layout.addWidget(apply_custom_btn, 3, 0, 1, 3)
        
        layout.addWidget(custom_group)
        
        # Reset to Default
        reset_group = QGroupBox("Reset")
        reset_layout = QHBoxLayout(reset_group)
        
        reset_btn = QPushButton("Reset to Windows Default")
        reset_btn.clicked.connect(self._reset_default)
        reset_layout.addWidget(reset_btn)
        
        reset_layout.addStretch()
        layout.addWidget(reset_group)
        
        layout.addStretch()
    
    def _choose_custom_color(self):
        """Choose custom accent color."""
        color = QColorDialog.getColor(QColor(self.custom_color), self)
        if color.isValid():
            self.custom_color = color.name()
            self.accent_preview.setStyleSheet(
                f"background-color: {self.custom_color}; border: 2px solid #ccc; border-radius: 4px;"
            )
    
    def _apply_theme(self, theme_id: str):
        """Apply a preset theme."""
        if self.theme_manager.apply_theme(theme_id):
            QMessageBox.information(self, "Success", f"Theme '{theme_id}' applied!")
        else:
            QMessageBox.critical(self, "Error", "Failed to apply theme.")
    
    def _apply_custom_theme(self):
        """Apply custom theme settings."""
        success = self.theme_manager.apply_custom_theme(
            accent_color=self.custom_color,
            light_mode=not self.dark_mode_check.isChecked(),
            transparency=self.transparency_check.isChecked(),
            colorize_taskbar=self.colorize_taskbar.isChecked(),
            colorize_start=self.colorize_start.isChecked()
        )
        
        if success:
            QMessageBox.information(self, "Success", "Custom theme applied!")
        else:
            QMessageBox.critical(self, "Error", "Failed to apply theme.")
    
    def _reset_default(self):
        """Reset to Windows default theme."""
        if self.theme_manager.apply_theme("default"):
            QMessageBox.information(self, "Success", "Reset to Windows default theme!")
        else:
            QMessageBox.critical(self, "Error", "Failed to reset theme.")


class IconsWidget(QWidget):
    """Widget for icon customization."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_manager = IconManager()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Warning
        warning = QLabel("⚠ Some changes require restarting Explorer to take effect.")
        warning.setStyleSheet("color: #d83b01; padding: 5px;")
        layout.addWidget(warning)
        
        # System Icons
        system_group = QGroupBox("System Icons")
        system_layout = QVBoxLayout(system_group)
        
        # Desktop Icons Visibility
        visibility_layout = QGridLayout()
        visibility_layout.addWidget(QLabel("Desktop Icons:"), 0, 0)
        
        self.icon_checks = {}
        icons = [
            ("computer", "This PC"),
            ("recycle_bin", "Recycle Bin"),
            ("user_files", "User Files"),
            ("network", "Network"),
            ("control_panel", "Control Panel"),
        ]
        
        row, col = 0, 1
        for icon_id, icon_name in icons:
            check = QCheckBox(icon_name)
            check.setChecked(True)
            self.icon_checks[icon_id] = check
            visibility_layout.addWidget(check, row, col)
            col += 1
            if col > 2:
                col = 1
                row += 1
        
        apply_visibility_btn = QPushButton("Apply Visibility")
        apply_visibility_btn.clicked.connect(self._apply_icon_visibility)
        visibility_layout.addWidget(apply_visibility_btn, row + 1, 0, 1, 3)
        
        system_layout.addLayout(visibility_layout)
        
        # Icon customization
        customize_layout = QHBoxLayout()
        customize_layout.addWidget(QLabel("Change Icon:"))
        
        self.icon_select = QComboBox()
        for icon_type in self.icon_manager.get_system_icon_list():
            info = self.icon_manager.get_icon_info(icon_type)
            if info:
                self.icon_select.addItem(info["name"], icon_type)
        customize_layout.addWidget(self.icon_select)
        
        browse_icon_btn = QPushButton("Browse .ico...")
        browse_icon_btn.clicked.connect(self._browse_icon)
        customize_layout.addWidget(browse_icon_btn)
        
        reset_icon_btn = QPushButton("Reset to Default")
        reset_icon_btn.clicked.connect(self._reset_icon)
        customize_layout.addWidget(reset_icon_btn)
        
        system_layout.addLayout(customize_layout)
        layout.addWidget(system_group)
        
        # Folder Icons
        folder_group = QGroupBox("Folder Icons")
        folder_layout = QVBoxLayout(folder_group)
        
        folder_info = QLabel("Change the icon for a specific folder:")
        folder_layout.addWidget(folder_info)
        
        folder_select_layout = QHBoxLayout()
        folder_select_layout.addWidget(QLabel("Folder:"))
        self.folder_icon_path = QLineEdit()
        self.folder_icon_path.setPlaceholderText("Select a folder...")
        folder_select_layout.addWidget(self.folder_icon_path)
        
        browse_folder_btn = QPushButton("Browse...")
        browse_folder_btn.clicked.connect(self._browse_folder_for_icon)
        folder_select_layout.addWidget(browse_folder_btn)
        folder_layout.addLayout(folder_select_layout)
        
        folder_icon_layout = QHBoxLayout()
        folder_icon_layout.addWidget(QLabel("Icon:"))
        self.folder_icon_file = QLineEdit()
        self.folder_icon_file.setPlaceholderText("Select an .ico file...")
        folder_icon_layout.addWidget(self.folder_icon_file)
        
        browse_folder_icon_btn = QPushButton("Browse...")
        browse_folder_icon_btn.clicked.connect(self._browse_folder_icon)
        folder_icon_layout.addWidget(browse_folder_icon_btn)
        
        apply_folder_btn = QPushButton("Apply")
        apply_folder_btn.clicked.connect(self._apply_folder_icon)
        folder_icon_layout.addWidget(apply_folder_btn)
        folder_layout.addLayout(folder_icon_layout)
        
        layout.addWidget(folder_group)
        
        # Refresh Icon Cache
        cache_group = QGroupBox("Icon Cache")
        cache_layout = QHBoxLayout(cache_group)
        
        cache_info = QLabel("Clear icon cache if icons appear incorrect:")
        cache_layout.addWidget(cache_info)
        
        refresh_cache_btn = QPushButton("Clear Icon Cache")
        refresh_cache_btn.clicked.connect(self._clear_icon_cache)
        cache_layout.addWidget(refresh_cache_btn)
        
        cache_layout.addStretch()
        layout.addWidget(cache_group)
        
        layout.addStretch()
    
    def _apply_icon_visibility(self):
        """Apply desktop icon visibility settings."""
        for icon_id, checkbox in self.icon_checks.items():
            self.icon_manager.show_desktop_icon(icon_id, checkbox.isChecked())
        
        QMessageBox.information(self, "Success", "Desktop icon visibility updated!")
    
    def _browse_icon(self):
        """Browse for icon file to change system icon."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            "",
            "Icons (*.ico);;All Files (*)"
        )
        if file_path:
            icon_type = self.icon_select.currentData()
            if self.icon_manager.set_system_icon(icon_type, file_path):
                QMessageBox.information(self, "Success", "Icon changed! Restart Explorer to see changes.")
            else:
                QMessageBox.critical(self, "Error", "Failed to change icon.")
    
    def _reset_icon(self):
        """Reset system icon to default."""
        icon_type = self.icon_select.currentData()
        if self.icon_manager.reset_system_icon(icon_type):
            QMessageBox.information(self, "Success", "Icon reset to default!")
        else:
            QMessageBox.critical(self, "Error", "Failed to reset icon.")
    
    def _browse_folder_for_icon(self):
        """Browse for folder to customize."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_icon_path.setText(folder)
    
    def _browse_folder_icon(self):
        """Browse for icon file for folder."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            "",
            "Icons (*.ico);;DLL Files (*.dll);;All Files (*)"
        )
        if file_path:
            self.folder_icon_file.setText(file_path)
    
    def _apply_folder_icon(self):
        """Apply icon to folder."""
        folder = self.folder_icon_path.text()
        icon = self.folder_icon_file.text()
        
        if not folder or not icon:
            QMessageBox.warning(self, "Error", "Please select both a folder and an icon.")
            return
        
        if self.icon_manager.change_folder_icon(folder, icon):
            QMessageBox.information(self, "Success", "Folder icon applied!")
        else:
            QMessageBox.critical(self, "Error", "Failed to apply folder icon.")
    
    def _clear_icon_cache(self):
        """Clear the icon cache."""
        reply = QMessageBox.question(
            self,
            "Confirm",
            "This will restart Explorer. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.icon_manager._clear_icon_cache()
            QMessageBox.information(self, "Success", "Icon cache cleared!")


class FontWidget(QWidget):
    """Widget for font customization."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.font_manager = FontManager()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Warning label
        warning = QLabel("⚠ Font changes require signing out and back in to take full effect.")
        warning.setStyleSheet("color: #d83b01; padding: 10px;")
        layout.addWidget(warning)
        
        # System Font Section
        system_group = QGroupBox("System UI Font")
        system_layout = QGridLayout(system_group)
        
        # Font selection
        system_layout.addWidget(QLabel("Font:"), 0, 0)
        self.font_combo = QComboBox()
        self.font_combo.addItems(self.font_manager.get_installed_fonts())
        self.font_combo.setCurrentText("Segoe UI")
        self.font_combo.setMinimumWidth(200)
        system_layout.addWidget(self.font_combo, 0, 1)
        
        # Font size
        system_layout.addWidget(QLabel("Size:"), 0, 2)
        self.font_size = QSpinBox()
        self.font_size.setRange(6, 24)
        self.font_size.setValue(9)
        system_layout.addWidget(self.font_size, 0, 3)
        
        # Apply button
        apply_font_btn = QPushButton("Apply System Font")
        apply_font_btn.clicked.connect(self._apply_system_font)
        system_layout.addWidget(apply_font_btn, 0, 4)
        
        # Element-specific font
        system_layout.addWidget(QLabel("Apply to:"), 1, 0)
        self.element_combo = QComboBox()
        self.element_combo.addItem("All Elements", "all")
        for element, description in self.font_manager.FONT_ELEMENTS.items():
            self.element_combo.addItem(description, element)
        system_layout.addWidget(self.element_combo, 1, 1, 1, 2)
        
        system_layout.setColumnStretch(5, 1)
        layout.addWidget(system_group)
        
        # Current Fonts Display
        current_group = QGroupBox("Current Font Settings")
        current_layout = QVBoxLayout(current_group)
        
        self.font_list = QListWidget()
        self._refresh_font_list()
        current_layout.addWidget(self.font_list)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_font_list)
        current_layout.addWidget(refresh_btn)
        
        layout.addWidget(current_group)
        
        # DPI Scaling
        dpi_group = QGroupBox("DPI Scaling")
        dpi_layout = QHBoxLayout(dpi_group)
        
        dpi_layout.addWidget(QLabel("Scaling:"))
        self.dpi_slider = QSlider(Qt.Orientation.Horizontal)
        self.dpi_slider.setRange(100, 200)
        self.dpi_slider.setValue(100)
        self.dpi_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.dpi_slider.setTickInterval(25)
        dpi_layout.addWidget(self.dpi_slider)
        
        self.dpi_label = QLabel("100%")
        self.dpi_slider.valueChanged.connect(lambda v: self.dpi_label.setText(f"{v}%"))
        dpi_layout.addWidget(self.dpi_label)
        
        apply_dpi_btn = QPushButton("Apply DPI")
        apply_dpi_btn.clicked.connect(self._apply_dpi)
        dpi_layout.addWidget(apply_dpi_btn)
        
        layout.addWidget(dpi_group)
        
        # Restore defaults
        restore_btn = QPushButton("Restore Default Fonts")
        restore_btn.clicked.connect(self._restore_defaults)
        layout.addWidget(restore_btn)
        
        layout.addStretch()
    
    def _refresh_font_list(self):
        """Refresh the current fonts list."""
        self.font_list.clear()
        current_fonts = self.font_manager.get_current_fonts()
        
        for element, info in current_fonts.items():
            description = self.font_manager.FONT_ELEMENTS.get(element, element)
            item_text = f"{description}: {info['name']} ({info['size']}pt)"
            self.font_list.addItem(item_text)
    
    def _apply_system_font(self):
        """Apply the selected system font."""
        font_name = self.font_combo.currentText()
        font_size = self.font_size.value()
        element = self.element_combo.currentData()
        
        if self.font_manager.set_ui_font(font_name, font_size, element):
            QMessageBox.information(
                self,
                "Success",
                f"Font changed to {font_name} ({font_size}pt).\n\n"
                "Please sign out and back in for changes to take full effect."
            )
            self._refresh_font_list()
        else:
            QMessageBox.critical(self, "Error", "Failed to change font.")
    
    def _apply_dpi(self):
        """Apply DPI scaling."""
        scaling = self.dpi_slider.value()
        
        if self.font_manager.change_dpi_scaling(scaling):
            QMessageBox.information(
                self,
                "Success",
                f"DPI scaling set to {scaling}%.\n\n"
                "Please sign out and back in for changes to take effect."
            )
        else:
            QMessageBox.critical(self, "Error", "Failed to change DPI scaling.")
    
    def _restore_defaults(self):
        """Restore default fonts."""
        reply = QMessageBox.question(
            self,
            "Confirm",
            "Restore all fonts to default?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.font_manager.restore_default_fonts():
                QMessageBox.information(
                    self,
                    "Success",
                    "Fonts restored to defaults.\n\n"
                    "Please sign out and back in for changes to take full effect."
                )
                self._refresh_font_list()
            else:
                QMessageBox.critical(self, "Error", "Failed to restore fonts.")


class PersonalizationTab(QWidget):
    """Combined personalization tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        tabs = QTabWidget()
        
        # Wallpaper tab (now includes video)
        tabs.addTab(WallpaperWidget(), "Wallpaper & Video")
        
        # Themes tab
        tabs.addTab(ThemesWidget(), "Themes & Colors")
        
        # Icons tab
        tabs.addTab(IconsWidget(), "Icons")
        
        # Fonts tab
        tabs.addTab(FontWidget(), "Fonts")
        
        layout.addWidget(tabs)
