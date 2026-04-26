"""
Custom font controls for WinTweaks.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Optional

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

SPI_GETNONCLIENTMETRICS = 0x0029
SPI_SETNONCLIENTMETRICS = 0x002A
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDCHANGE = 0x0002

LF_FACESIZE = 32
DEFAULT_CHARSET = 1
OUT_DEFAULT_PRECIS = 0
CLIP_DEFAULT_PRECIS = 0
CLEARTYPE_QUALITY = 5
DEFAULT_PITCH = 0
FF_DONTCARE = 0


class LOGFONTW(ctypes.Structure):
    _fields_ = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", wintypes.BYTE),
        ("lfUnderline", wintypes.BYTE),
        ("lfStrikeOut", wintypes.BYTE),
        ("lfCharSet", wintypes.BYTE),
        ("lfOutPrecision", wintypes.BYTE),
        ("lfClipPrecision", wintypes.BYTE),
        ("lfQuality", wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName", wintypes.WCHAR * LF_FACESIZE),
    ]


class NONCLIENTMETRICSW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("iBorderWidth", wintypes.INT),
        ("iScrollWidth", wintypes.INT),
        ("iScrollHeight", wintypes.INT),
        ("iCaptionWidth", wintypes.INT),
        ("iCaptionHeight", wintypes.INT),
        ("lfCaptionFont", LOGFONTW),
        ("iSmCaptionWidth", wintypes.INT),
        ("iSmCaptionHeight", wintypes.INT),
        ("lfSmCaptionFont", LOGFONTW),
        ("iMenuWidth", wintypes.INT),
        ("iMenuHeight", wintypes.INT),
        ("lfMenuFont", LOGFONTW),
        ("lfStatusFont", LOGFONTW),
        ("lfMessageFont", LOGFONTW),
        ("iPaddedBorderWidth", wintypes.INT),
    ]


class CustomFontsPanel(QWidget):
    """Panel that lets the user preview, load, and apply fonts to the app."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.default_app_font = QApplication.font()
        self.default_windows_metrics = self._read_non_client_metrics()
        self._setup_ui()
        self._refresh_preview()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        group = QGroupBox("Custom Fonts")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)

        description = QLabel(
            "Pick a system font or load your own font file and apply it to WinTweaks."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        group_layout.addWidget(description)

        system_note = QLabel(
            "Windows UI font changes are best-effort and may require sign out, restart, "
            "or restarting Explorer to fully appear everywhere."
        )
        system_note.setWordWrap(True)
        system_note.setStyleSheet(
            "padding: 8px 10px; background: #fff4ce; border: 1px solid #f1d27a; border-radius: 4px;"
        )
        group_layout.addWidget(system_note)

        form_layout = QFormLayout()

        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(sorted(QFontDatabase.families()))
        self.font_family_combo.currentTextChanged.connect(lambda *_: self._refresh_preview())
        form_layout.addRow("Font family", self.font_family_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 32)
        self.font_size_spin.setValue(self.default_app_font.pointSize() or 9)
        self.font_size_spin.valueChanged.connect(lambda *_: self._refresh_preview())
        form_layout.addRow("Font size", self.font_size_spin)

        group_layout.addLayout(form_layout)

        preview_title = QLabel("Preview")
        preview_title.setStyleSheet("font-weight: bold; color: #333333;")
        group_layout.addWidget(preview_title)

        self.preview_text = QLabel("The quick brown fox jumps over the lazy dog. 0123456789")
        self.preview_text.setWordWrap(True)
        self.preview_text.setStyleSheet(
            "padding: 10px; border: 1px solid #d8d8d8; background: white;"
        )
        group_layout.addWidget(self.preview_text)

        primary_buttons = QHBoxLayout()

        load_button = QPushButton("Load Font File")
        load_button.clicked.connect(self._load_font_file)
        primary_buttons.addWidget(load_button)

        apply_button = QPushButton("Apply Font")
        apply_button.clicked.connect(self._apply_font)
        primary_buttons.addWidget(apply_button)

        apply_windows_button = QPushButton("Apply to Windows UI")
        apply_windows_button.setToolTip(
            "Best-effort change for Windows system UI fonts. May require sign out or restart."
        )
        apply_windows_button.clicked.connect(self._apply_windows_ui_font)
        primary_buttons.addWidget(apply_windows_button)

        primary_buttons.addStretch()
        group_layout.addLayout(primary_buttons)

        secondary_buttons = QHBoxLayout()

        reset_button = QPushButton("Reset Default")
        reset_button.clicked.connect(self._reset_default_font)
        secondary_buttons.addWidget(reset_button)

        reset_windows_button = QPushButton("Reset Windows UI Font")
        reset_windows_button.setToolTip(
            "Restore the saved Windows system UI fonts from when WinTweaks started."
        )
        reset_windows_button.clicked.connect(self._reset_windows_ui_font)
        secondary_buttons.addWidget(reset_windows_button)

        restart_button = QPushButton("Restart WinTweaks")
        restart_button.setToolTip("Restart the app to make sure font changes are fully applied.")
        restart_button.clicked.connect(self._restart_application)
        secondary_buttons.addWidget(restart_button)

        secondary_buttons.addStretch()
        group_layout.addLayout(secondary_buttons)

        self.status_label = QLabel("Select a font to preview it before applying.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "padding: 8px 10px; background: #f7f7f7; border: 1px solid #e0e0e0; border-radius: 4px;"
        )
        group_layout.addWidget(self.status_label)

        layout.addWidget(group)

    def _selected_font(self) -> QFont:
        font = QFont(self.font_family_combo.currentText())
        font.setPointSize(self.font_size_spin.value())
        return font

    def _apply_font_globally(self, font: QFont) -> None:
        app = QApplication.instance()
        if app is None:
            return

        app.setFont(font)

        for widget in app.topLevelWidgets():
            widget.setFont(font)
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

        app.processEvents()

    def _current_dpi(self) -> float:
        app = QApplication.instance()
        if app is not None:
            screen = app.primaryScreen()
            if screen is not None:
                return float(screen.logicalDotsPerInch())
        return 96.0

    def _qfont_to_logfont(self, font: QFont) -> LOGFONTW:
        logfont = LOGFONTW()
        point_size = font.pointSizeF()
        if point_size <= 0:
            point_size = float(self.default_app_font.pointSize() or 9)

        logfont.lfHeight = -int(round(point_size * self._current_dpi() / 72.0))
        logfont.lfWidth = 0
        logfont.lfEscapement = 0
        logfont.lfOrientation = 0
        logfont.lfWeight = 700 if font.bold() else 400
        logfont.lfItalic = 1 if font.italic() else 0
        logfont.lfUnderline = 1 if font.underline() else 0
        logfont.lfStrikeOut = 1 if font.strikeOut() else 0
        logfont.lfCharSet = DEFAULT_CHARSET
        logfont.lfOutPrecision = OUT_DEFAULT_PRECIS
        logfont.lfClipPrecision = CLIP_DEFAULT_PRECIS
        logfont.lfQuality = CLEARTYPE_QUALITY
        logfont.lfPitchAndFamily = DEFAULT_PITCH | FF_DONTCARE
        logfont.lfFaceName = font.family()[: LF_FACESIZE - 1]
        return logfont

    def _copy_non_client_metrics(self, metrics: NONCLIENTMETRICSW) -> NONCLIENTMETRICSW:
        clone = NONCLIENTMETRICSW()
        ctypes.memmove(
            ctypes.byref(clone),
            ctypes.byref(metrics),
            ctypes.sizeof(NONCLIENTMETRICSW),
        )
        return clone

    def _read_non_client_metrics(self) -> Optional[NONCLIENTMETRICSW]:
        if not hasattr(ctypes, "windll"):
            return None

        metrics = NONCLIENTMETRICSW()
        metrics.cbSize = ctypes.sizeof(NONCLIENTMETRICSW)

        try:
            success = ctypes.windll.user32.SystemParametersInfoW(
                SPI_GETNONCLIENTMETRICS,
                metrics.cbSize,
                ctypes.byref(metrics),
                0,
            )
            if success:
                return metrics
        except Exception:
            return None

        return None

    def _write_non_client_metrics(self, metrics: NONCLIENTMETRICSW) -> bool:
        if not hasattr(ctypes, "windll"):
            return False

        try:
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETNONCLIENTMETRICS,
                ctypes.sizeof(NONCLIENTMETRICSW),
                ctypes.byref(metrics),
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
            )
            if result:
                app = QApplication.instance()
                if app is not None:
                    app.processEvents()
            return bool(result)
        except Exception:
            return False

    def _apply_windows_ui_font(self, *_args) -> None:
        font = self._selected_font()
        self._apply_font_globally(font)

        current_metrics = self._read_non_client_metrics()
        if current_metrics is None:
            QMessageBox.warning(
                self,
                "WinTweaks",
                "Could not read Windows UI font settings on this system.",
            )
            return

        metrics = self._copy_non_client_metrics(current_metrics)
        logfont = self._qfont_to_logfont(font)

        metrics.lfCaptionFont = logfont
        metrics.lfSmCaptionFont = logfont
        metrics.lfMenuFont = logfont
        metrics.lfStatusFont = logfont
        metrics.lfMessageFont = logfont

        if self._write_non_client_metrics(metrics):
            self.status_label.setText(
                f"Applied {font.family()} to Windows UI fonts. Sign out or restart may be needed."
            )
            QMessageBox.information(
                self,
                "WinTweaks",
                "Windows UI font settings updated.\n\n"
                "Some parts of Windows may require sign out, restart, or Explorer restart to refresh.",
            )
        else:
            QMessageBox.warning(
                self,
                "WinTweaks",
                "Could not update Windows UI font settings.",
            )

    def _reset_windows_ui_font(self, *_args) -> None:
        if self.default_windows_metrics is None:
            QMessageBox.warning(
                self,
                "WinTweaks",
                "No saved Windows UI font settings were available to restore.",
            )
            return

        if self._write_non_client_metrics(
            self._copy_non_client_metrics(self.default_windows_metrics)
        ):
            self.status_label.setText("Restored the saved Windows UI font settings.")
            QMessageBox.information(
                self,
                "WinTweaks",
                "Windows UI font settings restored.\n\n"
                "Sign out or restart may still be needed for all Windows surfaces to refresh.",
            )
        else:
            QMessageBox.warning(
                self,
                "WinTweaks",
                "Could not restore Windows UI font settings.",
            )

    def _refresh_preview(self) -> None:
        font = self._selected_font()
        self.preview_text.setFont(font)
        self.status_label.setText(f"Previewing {font.family()} at {font.pointSize()} pt.")

    def _load_font_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Font File",
            "",
            "Fonts (*.ttf *.otf *.ttc);;All Files (*)",
        )
        if not file_path:
            return

        font_id = QFontDatabase.addApplicationFont(file_path)
        if font_id == -1:
            QMessageBox.warning(
                self,
                "WinTweaks",
                "Could not load that font file.",
            )
            return

        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            family = families[0]
            if self.font_family_combo.findText(family) == -1:
                self.font_family_combo.addItem(family)
            self.font_family_combo.setCurrentText(family)

        self._refresh_preview()
        self.status_label.setText(f"Loaded font file: {file_path}")

    def _apply_font(self) -> None:
        font = self._selected_font()
        self._apply_font_globally(font)
        self.status_label.setText(
            f"Applied {font.family()} at {font.pointSize()} pt to the entire UI."
        )
        QMessageBox.information(
            self,
            "WinTweaks",
            "Font applied to the entire UI.",
        )

    def _reset_default_font(self) -> None:
        self._apply_font_globally(self.default_app_font)

        default_family = self.default_app_font.family()
        default_size = self.default_app_font.pointSize() or 9

        if self.font_family_combo.findText(default_family) != -1:
            self.font_family_combo.setCurrentText(default_family)
        self.font_size_spin.setValue(default_size)

        self._refresh_preview()
        self.status_label.setText("Restored the application default font.")
        QMessageBox.information(
            self,
            "WinTweaks",
            "Default font restored.",
        )

    def _restart_application(self) -> None:
        confirm = QMessageBox.question(
            self,
            "Restart WinTweaks",
            "Restart WinTweaks now to fully apply the current font?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            import os
            import subprocess
            import sys

            arguments = [sys.executable] + sys.argv
            if getattr(sys, "frozen", False):
                arguments = [sys.executable] + sys.argv[1:]

            subprocess.Popen(arguments, cwd=os.getcwd())
            QApplication.quit()
        except Exception as exc:
            QMessageBox.warning(
                self,
                "WinTweaks",
                f"Could not restart the app:\n{exc}",
            )
