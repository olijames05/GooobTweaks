"""
Video wallpaper beta panel for WinTweaks.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
)


class VideoWallpaperWindow(QWidget):
    """Frameless full-screen window that plays a video like a wallpaper."""

    def __init__(self, video_path: str, loop_enabled: bool = True, muted: bool = True, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.video_path = video_path
        self.loop_enabled = loop_enabled
        self.muted = muted
        self._setup_ui()
        self._load_video()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Video Wallpaper")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget, 1)

        self.overlay_label = QLabel("Press Esc to close")
        self.overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay_label.setStyleSheet(
            "padding: 8px 12px; background: rgba(0, 0, 0, 160); color: white; font-size: 11px;"
        )
        layout.addWidget(self.overlay_label)

        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(0.0 if self.muted else 0.8)

        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

    def _load_video(self) -> None:
        self.player.setSource(QUrl.fromLocalFile(self.video_path))
        self.player.play()

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self.loop_enabled:
            self.player.setPosition(0)
            self.player.play()

    def keyPressEvent(self, event) -> None:  # type: ignore[override]
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self.player.stop()
        super().closeEvent(event)


class VideoWallpaperPanel(QWidget):
    """Beta controls for selecting and previewing a video wallpaper."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.video_path: Optional[str] = None
        self.preview_window: Optional[VideoWallpaperWindow] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        group = QGroupBox("Video Wallpaper (Beta)")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)

        description = QLabel(
            "Choose a video and preview it as a wallpaper-style animation. "
            "This is a beta feature and uses a live preview window."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        group_layout.addWidget(description)

        self.video_path_label = QLabel("No video selected")
        self.video_path_label.setWordWrap(True)
        self.video_path_label.setStyleSheet("color: #444444;")
        group_layout.addWidget(self.video_path_label)

        button_row = QHBoxLayout()

        choose_button = QPushButton("Choose Video")
        choose_button.clicked.connect(self._choose_video)
        button_row.addWidget(choose_button)

        play_button = QPushButton("Play Preview")
        play_button.clicked.connect(self._play_preview)
        button_row.addWidget(play_button)

        wallpaper_button = QPushButton("Open Wallpaper Window")
        wallpaper_button.clicked.connect(self._open_wallpaper_window)
        button_row.addWidget(wallpaper_button)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self._stop_preview)
        button_row.addWidget(stop_button)

        button_row.addStretch()
        group_layout.addLayout(button_row)

        options_row = QHBoxLayout()

        self.loop_checkbox = QCheckBox("Loop video")
        self.loop_checkbox.setChecked(True)
        options_row.addWidget(self.loop_checkbox)

        self.mute_checkbox = QCheckBox("Mute audio")
        self.mute_checkbox.setChecked(True)
        options_row.addWidget(self.mute_checkbox)

        options_row.addStretch()
        group_layout.addLayout(options_row)

        preview_frame = QFrame()
        preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        preview_frame.setMinimumHeight(220)
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_widget = QVideoWidget()
        preview_layout.addWidget(self.preview_widget)
        group_layout.addWidget(preview_frame)

        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(0.0)

        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.preview_widget)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

        self.status_label = QLabel("Select a video to begin.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "padding: 8px 10px; background: #f7f7f7; border: 1px solid #e0e0e0; border-radius: 4px;"
        )
        group_layout.addWidget(self.status_label)

        layout.addWidget(group)

    def _choose_video(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Video Wallpaper",
            "",
            "Video Files (*.mp4 *.m4v *.mov *.avi *.mkv *.wmv *.webm);;All Files (*)",
        )
        if not file_path:
            return

        self.video_path = file_path
        self.video_path_label.setText(f"Selected video: {file_path}")
        self._load_selected_video()

    def _load_selected_video(self) -> None:
        if not self.video_path:
            return

        self.player.setSource(QUrl.fromLocalFile(self.video_path))
        self.status_label.setText("Video loaded. Press Play Preview or Open Wallpaper Window.")

    def _play_preview(self) -> None:
        if not self.video_path:
            self._show_error("Choose a video first.")
            return

        if self.player.source().isEmpty():
            self._load_selected_video()

        self.player.setMuted(self.mute_checkbox.isChecked())
        self.player.play()
        self.status_label.setText("Video wallpaper preview is playing.")

    def _open_wallpaper_window(self) -> None:
        if not self.video_path:
            self._show_error("Choose a video first.")
            return

        if self.preview_window is not None:
            self.preview_window.close()
            self.preview_window = None

        self.preview_window = VideoWallpaperWindow(
            self.video_path,
            loop_enabled=self.loop_checkbox.isChecked(),
            muted=self.mute_checkbox.isChecked(),
        )
        self.preview_window.showFullScreen()
        self.status_label.setText("Wallpaper window opened. Press Esc to close it.")

    def _stop_preview(self) -> None:
        self.player.stop()
        if self.preview_window is not None:
            self.preview_window.close()
            self.preview_window = None
        self.status_label.setText("Video wallpaper stopped.")

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self.loop_checkbox.isChecked():
            self.player.setPosition(0)
            self.player.play()

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "WinTweaks", message)
