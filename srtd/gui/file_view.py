#!/usr/bin/env python3

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from .themes import *

def create_file_tree_scroll_view(file_list: list[FileObject]):
    tree_widget = QWidget()
    tree_layout = QVBoxLayout(tree_widget)

    tree_widget.setStyleSheet(PastelGreen().get_style_sheet())
    tree_widget.setContentsMargins(0, 0, 0, 0)

    # Add file structure lines
    for i in range(21):
        file_line = QLabel("📁   directory_name")
        file_line.setStyleSheet("text-align: center")
        file_line.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        tree_layout.addWidget(file_line)

    scroll_area = QtWidgets.QScrollArea()
    scroll_area.setStyleSheet(PastelGreen().get_style_sheet())
    scroll_area.setWidgetResizable(True)  # Allow the widget inside to resize

    # Set the tree widget as the content of the scroll area
    scroll_area.setWidget(tree_widget)

    # Wait a little to allow for stuff to finish loading in
    QtCore.QTimer.singleShot(100, lambda: scroll_area.verticalScrollBar().setValue(
        scroll_area.verticalScrollBar().maximum()))

    return scroll_area
