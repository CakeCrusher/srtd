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

from themes import *


class FileExplorer(QWidget):
    def __init__(self, app, theme=Sand()):
        super().__init__()
        self.app = app
        self.theme = theme

        # Set the theme
        # Create layout for the file explorer
        self.main_layout = QHBoxLayout()

        # Create file tree view
        file_model = QFileSystemModel()
        file_model.setRootPath("")
        file_tree = QTreeView()
        file_tree.setModel(file_model)
        file_tree.setRootIndex(file_model.index(""))

        # Set tree view background color
        file_tree.setStyleSheet(Sand().get_style_sheet())

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

        #---------Suggestions Section ------------
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
            tree_widget.setContentsMargins(0,0,0,0)
            
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
        search_label = QLabel("Search:")
        search_bar = QLineEdit()
        search_button = QPushButton("Search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)

        # Add search bar layout
        right_column_layout.addLayout(search_layout)

        # Create checkbox
        self.checkbox = QCheckBox("Track State")
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)

        # Connect search button click to show message box
        search_button.clicked.connect(self.show_custom_window)

        # Create splitter to resize the file tree and preview area
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(file_tree)
        splitter.addWidget(QWidget())  # Add the right column layout here for preview and search

        # Set initial splitter sizes to 65% (file tree) and 35% (preview)
        total_width = self.width()  # Get the total width of the window
        file_tree_width = int(total_width * 0.65)  # 65% of total width
        preview_area_width = total_width - file_tree_width  # 35% of total width
        splitter.setSizes([file_tree_width, preview_area_width])

        # Add layouts to the main layout
        self.main_layout.addWidget(splitter)
        self.main_layout.addLayout(right_column_layout)  # Add right column layout (preview and search)
        self.main_layout.addWidget(self.checkbox)  # Add checkbox to the main layout

        # Set layout for the widget
        self.setLayout(self.main_layout)
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

    def show_custom_window(self):
        # Create a custom window
        window = QtWidgets.QDialog()
        window.setWindowTitle("Search Options")

        # Create a vertical layout for the window
        window_layout = QtWidgets.QVBoxLayout(window)


        lex_suggestion_layout = QHBoxLayout()
        lex_suggestion_label = QLabel("Lexical Suggestions:")
        lex_suggestion_layout.addWidget(lex_suggestion_label)

        theme = ForestGreen()
        lex_suggestion_label.setStyleSheet(
            f"background-color: {theme.secondary_color}; color: {theme.primary_color};")

        window_layout.addLayout(lex_suggestion_layout)

        # Create a QLabel with long text
        text_label = QtWidgets.QLabel(
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
            "This is a long text that will be displayed in the popup box.\n"
            "It will automatically scroll if it exceeds the available space.\n"
            "You can add more lines of text here as needed."
        )

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(text_label)
        scroll_area.setWidgetResizable(True)

        # Add the scroll area to the window layout
        window_layout.addWidget(scroll_area)

        # Create individual buttons
        ok_button = QPushButton("Ok")
        yes_to_all_button = QPushButton("Yes to All")
        cancel_button = QPushButton("Cancel")

        # Connect button signals to slots
        ok_button.clicked.connect(self.on_ok_clicked)
        yes_to_all_button.clicked.connect(self.on_yes_to_all_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)

        # Add buttons to the window layout
        window_layout.addWidget(ok_button)
        window_layout.addWidget(yes_to_all_button)
        window_layout.addWidget(cancel_button)

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
        self.show_custom_window()

