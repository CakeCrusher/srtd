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
    file_clicked = Signal(str)

    def __init__(self, file_list=None, bg_color_stylesheet=None, show_path=False, parent=None, has_checkboxes: bool = True):
        super().__init__(parent)

        self.file_list = file_list if file_list else []
        self.bg_color_stylesheet = bg_color_stylesheet if bg_color_stylesheet else PastelGreen().get_style_sheet()
        self.show_path = show_path
        self.has_checkboxes = has_checkboxes

        self.checkboxes = []  # Store checkboxes and their associated file objects

        self.file_clicked.connect(self.on_file_clicked)
        self.setup_ui()

    def setup_ui(self):
        tree_widget = QWidget()
        tree_layout = QVBoxLayout(tree_widget)

        tree_widget.setStyleSheet(self.bg_color_stylesheet)
        tree_widget.setContentsMargins(0, 0, 0, 0)

        for file in self.file_list:
            file_entry = QHBoxLayout()
            if self.has_checkboxes:
                check_box = QCheckBox()
                check_box.setStyleSheet(checkbox_styling)
                self.checkboxes.append((check_box, file))  # Store the checkbox with its file object
                file_entry.addWidget(check_box, 1)

            icon = "📁" if file.is_directory else "📄"
            text = file.path if self.show_path else file.name

            file_button = QPushButton(f"{icon} {text}")
            file_button.setStyleSheet("border: none; text-align: left;")
            file_button.clicked.connect(
                lambda checked, path=file.path: self.file_clicked.emit(path)
            )
            file_entry.addWidget(file_button, 9)

            tree_layout.addLayout(file_entry)

        if not self.file_list:
            print("no files")

        self.setWidgetResizable(True)
        self.setWidget(tree_widget)

        QTimer.singleShot(100, self.adjust_scroll_bar)

    def adjust_scroll_bar(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def rerender_tree_layout(self, file_list=[]):
        self.file_list = file_list

        tree_widget = self.widget()
        if tree_widget is not None:
            tree_layout = tree_widget.layout()
            if tree_layout is not None:
                while tree_layout.count():
                    item = tree_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            tree_widget.deleteLater()

        self.checkboxes.clear()  # Clear the old checkboxes
        self.setup_ui()

    def on_file_clicked(self, file_path):
        print(f"File clicked: {file_path}")
        self.chosen_dest_path = file_path

    def get_checked_files(self) -> List[FileObject]:
        """Returns a list of files that are checked."""
        return [file for checkbox, file in self.checkboxes if checkbox.isChecked()]

    def get_checked_items(self) -> List[str]:
        """Retrieve a list of checked file paths."""
        checked_items = []
        tree_widget = self.widget()
        if tree_widget:
            for i in range(tree_widget.layout().count()):
                item_layout = tree_widget.layout().itemAt(i)
                if item_layout and item_layout.layout():
                    checkbox = item_layout.layout().itemAt(0).widget()
                    if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                        file_button = item_layout.layout().itemAt(1).widget()
                        if isinstance(file_button, QPushButton):
                            checked_items.append(file_button.text().split(" ", 1)[-1])  # Extract file path or name
        return checked_items
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
