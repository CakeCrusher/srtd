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
from ..core import buildFileList, buildDestinationList
from ..filter import getMatches

from .themes import *

class FileExplorer(QWidget):
    def __init__(self, app, theme=Sand()):
        super().__init__()
        self.app = app
        self.theme = theme

        # Set the theme
        # Create layout for the file explorer
        self.main_layout = QHBoxLayout()

        # get file_list to work with
        self.source_list = buildFileList(os.path.expanduser("~/Pictures"))
        # Create file tree view
        file_layout = QVBoxLayout()

        file_model = QFileSystemModel()
        file_model.setRootPath("")
        file_tree = QTreeView()
        file_tree.setModel(file_model)
        file_tree.setRootIndex(file_model.index(""))

        for i in range(1, file_model.columnCount()):
            file_tree.hideColumn(i)

        file_tree.setColumnWidth(0, file_tree.width())

        # Set tree view background color
        file_tree.setStyleSheet(PastelYellow().get_style_sheet())

        file_layout.addWidget(file_tree)

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
                              "ex ea commodo consequat. Duis aute irure dolor in "
                              "reprehenderit in voluptate velit esse cillum dolore eu "
                              "fugiat nulla pariatur. Excepteur sint occaecat cupidatat "
                              "non proident, sunt in culpa qui officia deserunt mollit "
                              "anim id est laborum")
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

        # ---------Suggestions Section ------------
        # Create suggestions section
        suggestions_layout = QVBoxLayout()

        suggestions_title = QLabel("Suggestions")
        suggestions_title.setFixedHeight(25)
        suggestions_title.setStyleSheet(Sand().get_style_sheet())

        # Create suggestions content area
        suggestions_content = QWidget()
        suggestions_content_layout = QHBoxLayout(suggestions_content)

        # Create lexicographical and contextual suggestion boxes
        lex_box = QWidget()
        context_box = QWidget()
        lex_layout = QVBoxLayout(lex_box)
        context_layout = QVBoxLayout(context_box)

        # Add titles for suggestion boxes
        lex_title = QLabel("Lexicographical Suggestion")
        context_title = QLabel("Contextual Suggestion")

        lex_title.setFixedHeight(25)
        context_title.setFixedHeight(25)

        lex_title.setStyleSheet("background-color: #8BA890; padding: 3px;")
        context_title.setStyleSheet("background-color: #8BA890; padding: 3px;")

        lex_layout.addWidget(lex_title)
        context_layout.addWidget(context_title)

        def create_file_tree_widget():
            tree_widget = QWidget()
            tree_layout = QVBoxLayout(tree_widget)
            tree_widget.setStyleSheet("background-color: #E6EDDB")
            tree_widget.setContentsMargins(0, 0, 0, 0)

            # Create folder icon and structure
            folder_icon = QLabel("📁")
            folder_icon.setStyleSheet("font-size: 24px;")
            tree_layout.addWidget(folder_icon)

            # Add file structure lines
            for i in range(6):
                file_line = QLabel("└→📄 file_name")
                file_line.setStyleSheet("padding-left: 20px;")
                tree_layout.addWidget(file_line)

            return tree_widget

        lex_layout.addWidget(create_file_tree_widget())
        context_layout.addWidget(create_file_tree_widget())

        # Add suggestion boxes to content layout
        suggestions_content_layout.addWidget(lex_box)
        suggestions_content_layout.addWidget(context_box)

        # Add everything to suggestions layout
        suggestions_layout.addWidget(suggestions_title)
        suggestions_layout.addWidget(suggestions_content)

        # -----Combine preview and search into a single layout----
        right_column_layout.addLayout(preview_layout)
        right_column_layout.addLayout(suggestions_layout)

        # Create search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Filter Files:")
        self.search_bar = QLineEdit()
        search_button = QPushButton("Select Destination")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)

        # Add search bar layout
        right_column_layout.addLayout(search_layout)

        # handle search bar changes
        self.search_bar.textChanged.connect(self.on_text_changed)

        # Create checkbox
        # Connect search button click to show message box
        search_button.clicked.connect(self.show_confirmation_window)

        # Set size ratios for layouts in the main layout
        self.main_layout.addLayout(file_layout, 4)
        self.main_layout.addLayout(right_column_layout, 6)

        # Set layout for the widget
        self.setLayout(self.main_layout)
        self.setStyleSheet(Sand().get_style_sheet())
        self.resize(1080, 768)

    def on_checkbox_changed(self, state):
        # Handle checkbox state changes here
        print(f"Checkbox state changed to {state}")
        print(f"checkbox state type is {type(state)}")
        if state == Qt.CheckState.Unchecked.value:
            print("Checkbox is unchecked")
        elif state == Qt.CheckState.PartiallyChecked.value:
            print("Checkbox is partially checked?")
        else:
            print("Checkbox is checked")

    def show_confirmation_window(self):
        # Create a custom window
        window = QtWidgets.QDialog()
        window.setWindowTitle("Search Options")

        window.setStyleSheet(PastelGreen().get_style_sheet())

        # Create a vertical layout for the window
        window_layout = QtWidgets.QVBoxLayout(window)

        lex_suggestion_layout = QVBoxLayout()
        lex_suggestion_label = QLabel("Confirm moves:")
        lex_suggestion_label.setFixedHeight(25)
        lex_suggestion_layout.addWidget(lex_suggestion_label)
        lex_suggestion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lex_suggestion_label.setStyleSheet(ForestGreen().get_style_sheet() +
                                           "font-weight: bold;"
                                           " font-size: 20px;"
                                           " text-align: center;")

        window_layout.addLayout(lex_suggestion_layout)
        window.resize(800, 600)
        suggestion_content_layout = QHBoxLayout()
        # Instead, use a QLabel with word wrap
        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the widget inside to resize

        # Create a widget to hold the content
        content_widget = QtWidgets.QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Add the suggestion content to the widget
        suggestion_content_text = QtWidgets.QLabel(
            "File one\nFile two\nFile three\nFile four"
        )
        suggestion_content_text.setWordWrap(True)
        suggestion_content_text.setStyleSheet(PastelGreen().get_style_sheet())
        suggestion_content_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        suggestion_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        suggestion_content_text.setStyleSheet("font-size: 20px;")
        content_layout.addWidget(suggestion_content_text)

        # Set the content widget for the scroll area
        scroll_area.setWidget(content_widget)

        # Add the scroll area to the layout
        suggestion_content_graphic = QtWidgets.QLabel("→")
        suggestion_content_graphic.setStyleSheet("font-size: 75px;")
        suggestion_content_layout.addWidget(scroll_area, 5)

        dest_directory_layout = QVBoxLayout()
        dest_directory_layout.setSpacing(0)
        dest_directory_layout.setContentsMargins(0, 0, 0, 0)
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


        suggestion_content_layout.addWidget(suggestion_content_graphic, 2)
        suggestion_content_layout.addLayout(dest_directory_layout, 2)

        # Add the label directly to the layout
        window_layout.addLayout(suggestion_content_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Ok")
        yes_to_all_button = QPushButton("Yes to All")
        cancel_button = QPushButton("Cancel")

        # Connect button signals to slots
        ok_button.clicked.connect(self.on_ok_clicked)
        yes_to_all_button.clicked.connect(self.on_yes_to_all_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)

        # Add buttons to the window layout
        button_layout.addWidget(ok_button)
        button_layout.addWidget(yes_to_all_button)
        button_layout.addWidget(cancel_button)

        window_layout.addLayout(button_layout)
        # Show the window and start its event loop
        window.show()
        window.exec_()

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
        # business logic
        self.source_list = getMatches(target, self.source_list)

        # debug cli output
        cls()
        print("\n".join(stringify_file_list(self.source_list)))
        print("> ", target)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def stringify_file_list(file_list: str):
    # turn file list into list of strings of names
    return [file['name'] for file in file_list if 'name' in file]
