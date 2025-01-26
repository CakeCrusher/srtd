from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QScrollArea,
    QPushButton,
)
from typing import List
from ..schema import FileObject

from .themes import *
from ..schema import FileObject


class FileTreeScrollView(QScrollArea):
    # Define the `file_clicked` signal at the class level
    file_clicked = Signal(str)

    def __init__(self, file_list=[], bg_color_stylesheet=None, show_path=False, parent=None, has_checkboxes: bool = True):
        super().__init__(parent)

        # Set background color if provided
        self.bg_color_stylesheet = bg_color_stylesheet if bg_color_stylesheet else PastelGreen().get_style_sheet()

        self.file_list = file_list
        self.show_path = show_path
        self.has_checkboxes = has_checkboxes

        # Connect the signal to a slot that prints to the console
        self.file_clicked.connect(self.on_file_clicked)

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
            if self.has_checkboxes:
                check_box = QCheckBox()
                check_box.setStyleSheet(checkbox_styling)
                file_entry.addWidget(check_box, 1)

            icon = "📁" if file.is_directory else "📄"
            text = file.path if self.show_path else file.name

            # Use QPushButton for clickable behavior
            file_button = QPushButton(f"{icon} {text}")
            file_button.setStyleSheet("border: none; text-align: left;")

            # Pass the current file path explicitly using a default argument
            file_button.clicked.connect(
                lambda checked, path=file.path: self.file_clicked.emit(path)
            )
            file_entry.addWidget(file_button, 9)

            tree_layout.addLayout(file_entry)

        if not self.file_list:
            print("no files")

        self.setWidgetResizable(True)  # Allow the widget inside to resize
        self.setWidget(tree_widget)  # Set the tree widget as the content of the scroll area

        # Simulate loading delay (if needed)
        QTimer.singleShot(100, self.adjust_scroll_bar)

    def adjust_scroll_bar(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def rerender_tree_layout(self, file_list=[]):
        # replace file list
        self.file_list = file_list

        tree_widget = self.widget()  # Get the current widget in the scroll area
        if tree_widget is not None:
            tree_layout = tree_widget.layout()
            if tree_layout is not None:
                while tree_layout.count():
                    item = tree_layout.takeAt(0)  # Take the first item from the layout
                    if item.widget():
                        item.widget().deleteLater()  # If the item is a widget, delete it
            tree_widget.deleteLater()  # Finally, delete the tree widget itself

        self.setup_ui()  # Optionally re-setup the UI if needed

    def on_file_clicked(self, file_path):
        # Print the clicked file path to the console
        print(f"File clicked: {file_path}")

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