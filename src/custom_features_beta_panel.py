"""
Custom features beta panel for WinTweaks.

This panel lets the user define their own registry-based tweaks.
"""

from __future__ import annotations

from typing import Optional, Any

import winreg
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from registry_utils import (
    delete_registry_value,
    is_admin,
    read_registry_value,
    write_registry_value,
)


class CustomFeaturesBetaPanel(QWidget):
    """Beta panel for creating custom registry modifications."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self._refresh_status()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        group = QGroupBox("Custom Features (Beta)")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)

        description = QLabel(
            "Create your own registry-based tweaks. This is an advanced beta area, "
            "so use it carefully and double-check paths and values before applying."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        group_layout.addWidget(description)

        warning = QLabel(
            "Warning: bad registry values can cause unexpected behavior. "
            "Some changes may require restart or sign-out."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "padding: 8px 10px; background: #fff4e5; border: 1px solid #f0c36d; border-radius: 4px; color: #7a4b00;"
        )
        group_layout.addWidget(warning)

        form = QFormLayout()

        self.feature_name_edit = QLineEdit("Custom Registry Feature")
        self.feature_name_edit.setPlaceholderText("Optional label for your tweak")
        form.addRow("Feature name", self.feature_name_edit)

        self.hive_combo = QComboBox()
        self.hive_combo.addItem("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER)
        self.hive_combo.addItem("HKEY_LOCAL_MACHINE", winreg.HKEY_LOCAL_MACHINE)
        self.hive_combo.addItem("HKEY_CLASSES_ROOT", winreg.HKEY_CLASSES_ROOT)
        form.addRow("Registry hive", self.hive_combo)

        self.key_path_edit = QLineEdit()
        self.key_path_edit.setPlaceholderText(r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
        form.addRow("Key path", self.key_path_edit)

        self.value_name_edit = QLineEdit()
        self.value_name_edit.setPlaceholderText("ExampleValueName")
        form.addRow("Value name", self.value_name_edit)

        self.value_type_combo = QComboBox()
        self.value_type_combo.addItem("REG_DWORD", winreg.REG_DWORD)
        self.value_type_combo.addItem("REG_SZ", winreg.REG_SZ)
        self.value_type_combo.addItem("REG_EXPAND_SZ", winreg.REG_EXPAND_SZ)
        self.value_type_combo.addItem("REG_BINARY", winreg.REG_BINARY)
        self.value_type_combo.currentIndexChanged.connect(self._refresh_status)
        form.addRow("Value type", self.value_type_combo)

        self.enabled_value_edit = QLineEdit("1")
        self.enabled_value_edit.setPlaceholderText("Value written when enabled/applied")
        form.addRow("Enabled value", self.enabled_value_edit)

        self.disabled_value_edit = QLineEdit("0")
        self.disabled_value_edit.setPlaceholderText("Value written when disabled/reverted")
        form.addRow("Disabled value", self.disabled_value_edit)

        self.delete_on_disable_checkbox = QCheckBox("Delete value when disabled instead of writing the disabled value")
        self.delete_on_disable_checkbox.setChecked(False)
        form.addRow("", self.delete_on_disable_checkbox)

        group_layout.addLayout(form)

        button_row = QHBoxLayout()

        apply_enabled_button = QPushButton("Apply Enabled")
        apply_enabled_button.clicked.connect(lambda: self._apply_value(True))
        button_row.addWidget(apply_enabled_button)

        apply_disabled_button = QPushButton("Apply Disabled")
        apply_disabled_button.clicked.connect(lambda: self._apply_value(False))
        button_row.addWidget(apply_disabled_button)

        read_button = QPushButton("Read Current")
        read_button.clicked.connect(self._read_current_value)
        button_row.addWidget(read_button)

        clear_button = QPushButton("Clear Value")
        clear_button.clicked.connect(self._clear_value)
        button_row.addWidget(clear_button)

        button_row.addStretch()
        group_layout.addLayout(button_row)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "padding: 8px 10px; background: #f7f7f7; border: 1px solid #e0e0e0; border-radius: 4px;"
        )
        group_layout.addWidget(self.status_label)

        layout.addWidget(group)

    def _refresh_status(self) -> None:
        hive_name = self.hive_combo.currentText()
        value_type_name = self.value_type_combo.currentText()
        self.status_label.setText(
            f"Ready to edit {hive_name} values as {value_type_name}. "
            "Use Apply Enabled / Apply Disabled to write your custom tweak."
        )

    def _selected_hive(self) -> int:
        return self.hive_combo.currentData()

    def _selected_value_type(self) -> int:
        return self.value_type_combo.currentData()

    def _feature_label(self) -> str:
        name = self.feature_name_edit.text().strip()
        return name if name else "Custom Registry Feature"

    def _validate_inputs(self) -> bool:
        key_path = self.key_path_edit.text().strip()
        if not key_path:
            self._show_error("Enter a registry key path.")
            return False

        # Allow value name to be blank for the default value, but keep a warning.
        if self._selected_hive() == winreg.HKEY_LOCAL_MACHINE and not is_admin():
            reply = QMessageBox.question(
                self,
                "Administrator required",
                "This tweak targets HKEY_LOCAL_MACHINE. Continue without administrator privileges?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return False

        return True

    def _parse_value(self, raw_value: str) -> Any:
        value_type = self._selected_value_type()

        if value_type == winreg.REG_DWORD:
            if not raw_value.strip():
                return 0
            try:
                return int(raw_value, 0)
            except ValueError:
                raise ValueError("DWORD values must be numeric.")

        if value_type == winreg.REG_BINARY:
            cleaned = raw_value.replace(" ", "").replace(",", "").strip()
            if not cleaned:
                return b""
            if len(cleaned) % 2 != 0:
                raise ValueError("Binary values must contain an even number of hex characters.")
            try:
                return bytes.fromhex(cleaned)
            except ValueError as exc:
                raise ValueError("Binary values must be valid hex bytes.") from exc

        return raw_value

    def _apply_value(self, enabled: bool) -> None:
        if not self._validate_inputs():
            return

        raw_value = self.enabled_value_edit.text().strip() if enabled else self.disabled_value_edit.text().strip()
        value_name = self.value_name_edit.text().strip()
        if not value_name:
            value_name = ""

        key_path = self.key_path_edit.text().strip()
        hive = self._selected_hive()
        value_type = self._selected_value_type()

        try:
            if not enabled and self.delete_on_disable_checkbox.isChecked():
                if delete_registry_value(hive, key_path, value_name):
                    self.status_label.setText(
                        f"{self._feature_label()}: deleted the registry value at {key_path}."
                    )
                    return
                self._show_error("Failed to delete the registry value.")
                return

            value = self._parse_value(raw_value)
        except ValueError as exc:
            self._show_error(str(exc))
            return

        success = write_registry_value(hive, key_path, value_name, value, value_type)
        if success:
            state = "enabled" if enabled else "disabled"
            self.status_label.setText(
                f"{self._feature_label()} {state}: wrote {repr(value)} to {key_path}."
            )
        else:
            self._show_error("Failed to write the registry value.")

    def _read_current_value(self) -> None:
        if not self._validate_inputs():
            return

        hive = self._selected_hive()
        key_path = self.key_path_edit.text().strip()
        value_name = self.value_name_edit.text().strip()
        if not value_name:
            value_name = ""

        current = read_registry_value(hive, key_path, value_name, default=None)
        if current is None:
            self.status_label.setText("No current registry value was found.")
            return

        self.status_label.setText(f"Current registry value: {repr(current)}")

    def _clear_value(self) -> None:
        if not self._validate_inputs():
            return

        hive = self._selected_hive()
        key_path = self.key_path_edit.text().strip()
        value_name = self.value_name_edit.text().strip()
        if not value_name:
            value_name = ""

        success = delete_registry_value(hive, key_path, value_name)
        if success:
            self.status_label.setText("Registry value cleared.")
        else:
            self._show_error("Failed to clear the registry value.")

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "WinTweaks", message)
