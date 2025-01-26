#!/usr/bin/env python3

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel, QHBoxLayout, QCheckBox, QScrollArea
)
from typing import List
from ..schema import FileObject

from .themes import *
from ..schema import FileObject


class FileTreeScrollView(QScrollArea):
    def __init__(self, file_list=[], bg_color_stylesheet=None, show_path=False, parent=None):
        super().__init__(parent)

        # Set background color if provided
        self.bg_color_stylesheet = bg_color_stylesheet if bg_color_stylesheet else PastelGreen().get_style_sheet()

        self.file_list = file_list
        self.show_path = show_path

        self.setup_ui()

    def setup_ui(self):
        # Create the tree widget and layout
        tree_widget = QWidget()
        tree_layout = QVBoxLayout(tree_widget)

        tree_widget.setStyleSheet(self.bg_color_stylesheet)
        tree_widget.setContentsMargins(0, 0, 0, 0)

        # Add file structure lines
        for file in self.file_list:
            file_entry = QHBoxLayout()
            check_box = QCheckBox()
            check_box.setStyleSheet(checkbox_styling)
            file_entry.addWidget(check_box, 1)
            icon = "📁" if file.is_directory else "📄"
            text = file.path if self.show_path else file.name
            file_line = QLabel(f"{icon} {text}")
            file_line.setStyleSheet("text-align: center;")
            file_line.setAlignment(Qt.AlignmentFlag.AlignLeft)
            file_entry.addWidget(file_line, 9)

            tree_layout.addLayout(file_entry)

        if not self.file_list:
            print("no files")

        self.setWidgetResizable(True)  # Allow the widget inside to resize
        self.setWidget(tree_widget)  # Set the tree widget as the content of the scroll area

        # Simulate loading delay (if needed)
        QTimer.singleShot(100, self.adjust_scroll_bar)

    def adjust_scroll_bar(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

checkbox_styling = """
            QCheckBox {
                background-color: #f0f0f0;
                border: 1px solid #888;
                padding: 4px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #888;
                border-radius: 3px;
                background-color: #fff;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:unchecked {
                background-color: #fff;
                border-color: #888;
            }
        """
