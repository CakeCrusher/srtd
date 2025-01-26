from PySide6 import QtCore
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
    QCheckBox
)

class FileExplorer(QWidget):
    def __init__(self, theme):
        super().__init__()
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
        file_tree.hideColumn(1)
        file_tree.hideColumn(2)
        file_tree.hideColumn(3)

        # Set tree view background color
        file_tree.setStyleSheet(f"background-color: {theme.secondary_color};")

        # Create file preview area
        preview_layout = QVBoxLayout()

        # Add title
        preview_title = QLabel("Preview & Summary")
        preview_title.setStyleSheet("background-color: #FFE4C4; padding: 5px;")

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


        # Create search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_bar = QLineEdit()
        search_button = QPushButton("Search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)

        # Create checkbox
        self.checkbox = QCheckBox("Track State")
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)

        # Create splitter to resize the file tree and preview area
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(file_tree)
        splitter.addWidget(QWidget())  # Placeholder for preview area

        # Set initial splitter sizes (adjust as needed)
        splitter.setSizes([700, 300])  # Example: 70% for file tree, 30% for preview

        # Combine preview and search into a single layout
        preview_and_search_layout = QVBoxLayout()
        preview_and_search_layout.addLayout(preview_layout)
        preview_and_search_layout.addLayout(search_layout)

        # Add layouts to main layout
        self.main_layout.addWidget(splitter)
        self.main_layout.addLayout(preview_and_search_layout)
        self.main_layout.addWidget(self.checkbox)  # Add checkbox to the main layout

        # Set layout for the widget
        self.setLayout(self.main_layout)

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