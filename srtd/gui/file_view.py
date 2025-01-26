#!/usr/bin/env python3

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel, QHBoxLayout, QCheckBox,
)

from .themes import *
from ..schema import FileObject

def create_file_tree_scroll_view(file_list: list[FileObject]=[], bg_color_stylesheet=PastelGreen().get_style_sheet()):
    tree_widget = QWidget()
    tree_layout = QVBoxLayout(tree_widget)

    tree_widget.setStyleSheet(bg_color_stylesheet)
    tree_widget.setContentsMargins(0, 0, 0, 0)

    # Add file structure lines
    for file in file_list:
        file_entry = QHBoxLayout()
        check_box = QCheckBox()
        check_box.setStyleSheet("""
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
        """)
        file_entry.addWidget(check_box, 1)
        icon = "📁" if file.is_directory else "📄"
        file_line = QLabel(f"{icon} {file.name}")
        file_line.setStyleSheet("text-align: center")
        file_line.setAlignment(
            Qt.AlignmentFlag.AlignLeft)
        file_entry.addWidget(file_line, 9)

        tree_layout.addLayout(file_entry)

    if len(file_list) == 0:
        print("no files")

    scroll_area = QtWidgets.QScrollArea()
    scroll_area.setStyleSheet(bg_color_stylesheet)
    scroll_area.setWidgetResizable(True)  # Allow the widget inside to resize

    # Set the tree widget as the content of the scroll area
    scroll_area.setWidget(tree_widget)

    # Wait a little to allow for stuff to finish loading in
    QtCore.QTimer.singleShot(100, lambda: scroll_area.verticalScrollBar().setValue(
        scroll_area.verticalScrollBar().maximum()))

    return scroll_area
