from typing import List
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTreeView,
    QFileSystemModel,
    QSplitter,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QMessageBox
)

import os

from srtd.schema import FileObject
from ..core import buildFileList, buildDestinationList
from ..filter import getMatches, getMatchesSemantic
from .file_view import FileTreeScrollView

from .themes import *


class FileExplorer(QWidget):
    def __init__(self, app, theme=Sand()):
        super().__init__()
        self.app = app
        self.theme = theme

        self.confirmation_window = None

        # Set the theme
        # Create layout for the file explorer
        self.main_layout = QHBoxLayout()

        # get file_list to work with
        self.source_list = buildFileList(os.path.expanduser("~/Pictures"))
        self.semantic_source_list = []
        # Create file tree view
        file_layout = QVBoxLayout()
        # Create source selection area
        source_selection_layout = QHBoxLayout()
        source_selection_label = QLabel("Source Folder:")
        source_selection_edit = QLineEdit()
        source_select_button = QPushButton("Select folder")

        # Connect source_select_button to update source directory and rebuild file list
        source_select_button.clicked.connect(
            lambda: self.on_source_folder_selected(source_selection_edit.text()))

        source_selection_layout.addWidget(source_selection_label)
        source_selection_layout.addWidget(source_selection_edit)
        source_selection_layout.addWidget(source_select_button)
        file_layout.addLayout(source_selection_layout)

        # Create file tree view using the source list
        file_layout.addWidget(FileTreeScrollView(self.source_list,
                        PastelYellow().get_style_sheet()))

        right_column_layout = QVBoxLayout()
        # Create file preview area
        preview_layout = QVBoxLayout()

        # Add title
        preview_title = QLabel("Preview & Summary")
        preview_title.setFixedHeight(25)
        preview_title.setStyleSheet(Sand().get_style_sheet())

        # Create preview content area
        preview_content = QWidget()
        preview_content_layout = QHBoxLayout(preview_content)

        # Add preview icon area (light blue square)
        preview_icon = QLabel("📄")
        preview_icon.setFixedSize(200, 200)
        preview_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_icon.setStyleSheet("font-size: 48px;")
        preview_icon.setStyleSheet("background-color: #B0E0E0;")

        # Create summary text
        summary_text = QLabel("Summary:\nLorem ipsum dolor sit amet, consectetur "
                              "adipiscing elit. Sed do eiusmod tempor incididunt ut "
                              "labore et dolore magna aliqua. Ut enim ad minim veniam, "
                              "quis nostrud exercitation ullamco laboris nisi ut aliquip "
                              "ex ea commodo consequat.")
        summary_text.setWordWrap(True)

        # Stack icon and preview
        icon_layout = QVBoxLayout()
        icon_layout.addWidget(preview_icon)

        # Add widgets to preview content layout
        preview_content_layout.addLayout(icon_layout)
        preview_content_layout.addWidget(summary_text)

        # Add everything to main preview layout
        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(preview_content)
        preview_content.setMaximumHeight(240)

        # Suggestions Section
        suggestions_layout = QVBoxLayout()
        suggestions_title = QLabel("Suggestions")
        suggestions_title.setFixedHeight(25)
        suggestions_title.setStyleSheet(Sand().get_style_sheet())

        # Create suggestions content area
        suggestions_content = QWidget()
        suggestions_content_layout = QHBoxLayout(suggestions_content)

        # Create suggestion boxes
        lex_box = QWidget()
        # context_box = QWidget()
        lex_layout = QVBoxLayout(lex_box)
        # context_layout = QVBoxLayout(context_box)

        # Add titles for suggestion boxes
        lex_title = QLabel("Destination Folders")
        # context_title = QLabel("Contextual Suggestion")

        lex_title.setFixedHeight(25)
        # context_title.setFixedHeight(25)

        lex_title.setStyleSheet("background-color: #8BA890; padding: 3px;")
        # context_title.setStyleSheet("background-color: #8BA890; padding: 3px;")

        lex_layout.addWidget(lex_title)
        # context_layout.addWidget(context_title)

        # get list of destinations for use
        destination_list = buildDestinationList(["~/Documents", "~/Downloads", "~/School"])

        lex_layout.addWidget(FileTreeScrollView(destination_list, show_path=True))
        # context_layout.addWidget(create_file_tree_scroll_view())

        suggestions_content_layout.addWidget(lex_box)
        # suggestions_content_layout.addWidget(context_box)

        suggestions_layout.addWidget(suggestions_title)
        suggestions_layout.addWidget(suggestions_content)

        # Combine preview and suggestions
        right_column_layout.addLayout(preview_layout)
        right_column_layout.addLayout(suggestions_layout)

        # Search bar layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Filter Files:")
        self.search_bar = QLineEdit()
        search_button = QPushButton("Select Destination")
        semantic_search_button = QPushButton("Semantic Search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(semantic_search_button)
        search_layout.addWidget(search_button)

        # Add search bar layout
        right_column_layout.addLayout(search_layout)

        # Connect search bar changes
        self.search_bar.textChanged.connect(self.on_text_changed)

        # handle semantic search button changes
        semantic_search_button.clicked.connect(self.on_semantic_search_clicked)

        # Create checkbox
        # Connect search button click to show message box

        search_button.clicked.connect(self.show_confirmation_window)

        # Add layouts to the main layout
        self.main_layout.addLayout(file_layout, 4)
        self.main_layout.addLayout(right_column_layout, 6)

        # Set layout for the widget
        self.setLayout(self.main_layout)
        self.setStyleSheet(Sand().get_style_sheet())
        self.resize(1080, 768)

    # Handlers for various button clicks
    def on_checkbox_changed(self, state):
        if state == Qt.CheckState.Unchecked.value:
            print("Checkbox is unchecked")
        elif state == Qt.CheckState.PartiallyChecked.value:
            print("Checkbox is partially checked?")
        else:
            print("Checkbox is checked")

    def on_semantic_search_clicked(self):
        target = self.search_bar.text()
        self.semantic_source_list = getMatchesSemantic(target, [])
        # print("Semantic search button clicked", [file.path for file in self.semantic_source_list])

    def show_confirmation_window(self):
        if self.confirmation_window and self.confirmation_window.isVisible():
            self.confirmation_window.raise_()
            self.confirmation_window.activateWindow()
            return

        self.confirmation_window = QtWidgets.QDialog(self)
        self.confirmation_window.setWindowTitle("Search Options")
        self.confirmation_window.setStyleSheet(PastelGreen().get_style_sheet())

        window_layout = QtWidgets.QVBoxLayout(self.confirmation_window)
        lex_suggestion_layout = QVBoxLayout()
        lex_suggestion_label = QLabel("Confirm moves:")
        lex_suggestion_label.setFixedHeight(25)
        lex_suggestion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lex_suggestion_label.setStyleSheet(
            ForestGreen().get_style_sheet() + "font-weight: bold; font-size: 20px;")

        window_layout.addLayout(lex_suggestion_layout)
        suggestion_content_layout = QHBoxLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget()
        content_layout = QVBoxLayout(content_widget)

        suggestion_content_text = QtWidgets.QLabel("File one\nFile two\nFile three\nFile four\n")
        suggestion_content_text.setWordWrap(True)
        suggestion_content_text.setStyleSheet(PastelGreen().get_style_sheet())
        suggestion_content_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(suggestion_content_text)

        scroll_area.setWidget(content_widget)

        suggestion_content_graphic = QtWidgets.QLabel("→")
        suggestion_content_graphic.setStyleSheet("font-size: 75px;")
        suggestion_content_layout.addWidget(scroll_area, 5)
        suggestion_content_layout.addWidget(suggestion_content_graphic, 2)

        dest_directory_layout = QVBoxLayout()
        dest_directory_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dest_directory_image = QtWidgets.QLabel("📁")
        dest_directory_image.setStyleSheet(PastelGreen().get_style_sheet())
        dest_directory_image.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        dest_directory_image.setStyleSheet("font-size: 48px;")
        dest_directory_layout.addWidget(dest_directory_image)

        dest_directory_text = QtWidgets.QLabel("Destination Directory TODO:")
        dest_directory_text.setWordWrap(True)
        dest_directory_text.setStyleSheet(PastelGreen().get_style_sheet())
        dest_directory_layout.addWidget(dest_directory_text)

        suggestion_content_layout.addLayout(dest_directory_layout, 2)

        window_layout.addLayout(suggestion_content_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Ok")
        yes_to_all_button = QPushButton("Yes to All")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.on_ok_clicked)
        yes_to_all_button.clicked.connect(self.on_yes_to_all_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(yes_to_all_button)
        button_layout.addWidget(cancel_button)

        window_layout.addLayout(button_layout)

        self.confirmation_window.show()
        self.confirmation_window.exec()

        self.confirmation_window.finished.connect(self.on_message_box_result)

    def reset_confirmation_window(self):
        self.confirmation_window = None

    def on_ok_clicked(self):
        print("Ok button clicked")

    def on_yes_to_all_clicked(self):
        print("Yes to All button clicked")

    def on_cancel_clicked(self):
        print("Cancel button clicked")

    def on_message_box_result(self):
        self.show_confirmation_window()

    def on_text_changed(self):
        target = self.search_bar.text()
        self.source_list = getMatches(target, self.source_list)
        cls()
        print("\n".join(stringify_file_list(self.source_list)))
        print("> ", target)

    def on_source_folder_selected(self, source_dir):
        selected_dir = source_dir.strip()
        if not selected_dir:
            print("Please enter a source directory path")
            return
        res = buildFileList(selected_dir)
        if res is None:
            return
        self.source_list = res
        print(f"Source directory updated to: {selected_dir}")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def stringify_file_list(file_list: List[FileObject]):
    # turn file list into list of strings of names
    return [file.name for file in file_list]
