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
    QCheckBox,
    QMessageBox, QDialogButtonBox
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

        right_column_layout = QVBoxLayout()
        # Create file preview area
        preview_layout = QVBoxLayout()
        preview_area = QLabel()
        preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_area.setText("File Preview")
        preview_layout.addWidget(preview_area)

        # Combine preview and search into a single layout
        right_column_layout.addLayout(preview_layout)

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
        search_button.clicked.connect(self.show_message_box)

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

    def show_message_box(self) -> QMessageBox.ButtonRole:
        # Create and show a message box with three buttons in the desired order
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Search")
        msg_box.setText("Choose an action:")

        # Define the buttons
        ok_button = QPushButton("Ok")
        yes_to_all_button = QPushButton("Yes to All")
        cancel_button = QPushButton("Cancel")

        # Add buttons in the desired order
        msg_box.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
        msg_box.addButton(yes_to_all_button, QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton(cancel_button, QMessageBox.ButtonRole.RejectRole)

        # Show the message box and get the result
        result = msg_box.exec()

        # Return the result
        return result

    def on_message_box_result(self):
        # Call show_message_box and get the result
        result = self.show_message_box()

        # Handle the result
        if result == QMessageBox.ButtonRole.RejectRole:
            print("Cancel button clicked")
        elif result == QMessageBox.ButtonRole.ActionRole:
            print("Yes to All button clicked")
        elif result == QMessageBox.ButtonRole.AcceptRole:
            print("Ok button clicked")
        else:
            print(f"Unexpected result: {result}")