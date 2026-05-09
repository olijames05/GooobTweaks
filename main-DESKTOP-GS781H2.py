import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from main_window import MainWindow


def main():
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("WinTweaks")
    app.setApplicationVersion("2.0.0")
    
    # Set application font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Set stylesheet for modern look
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            margin-top: 12px;
            padding-top: 10px;
            background-color: white;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #106ebe;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QLabel {
            color: #333333;
        }
        QComboBox {
            padding: 5px;
            border: 1px solid #cccccc;
            background-color: white;
        }
        QSpinBox {
            padding: 5px;
            border: 1px solid #cccccc;
        }
        QListWidget {
            border: 1px solid #cccccc;
            background-color: white;
        }
        QListWidget::item {
            padding: 10px;
            border-bottom: 1px solid #eeeeee;
        }
        QListWidget::item:selected {
            background-color: #0078d4;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #e5f3ff;
        }
        QScrollArea {
            border: none;
        }
        QTabWidget::pane {
            border: 1px solid #cccccc;
        }
        QTabBar::tab {
            padding: 8px 14px;
            border: 1px solid #cccccc;
            border-bottom: none;
            background-color: #e8e8e8;
            color: #333333;
        }
        QTabBar::tab:selected {
            background-color: #0078d4;
            color: white;
        }
        QTabBar::tab:hover:!selected {
            background-color: #d0d0d0;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
