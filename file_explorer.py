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
)



class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout for the file explorer
        main_layout = QHBoxLayout()

        # Create file tree view
        file_model = QFileSystemModel()
        file_model.setRootPath("")
        file_tree = QTreeView()
        file_tree.setModel(file_model)
        file_tree.setRootIndex(file_model.index(""))
        file_tree.hideColumn(1)
        file_tree.hideColumn(2)
        file_tree.hideColumn(3)

        file_tree.setStyleSheet("background-color: #FF0000;") #red

        # Create file preview area
        preview_layout = QVBoxLayout()
        preview_area = QLabel()
        preview_area.setAlignment(Qt.AlignCenter)
        preview_area.setText("File Preview")
        preview_layout.addWidget(preview_area)

        # Create search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_bar = QLineEdit()
        search_button = QPushButton("Search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)

        # Create splitter to resize the file tree and preview area
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(file_tree)
        splitter.addWidget(QWidget())  # Placeholder for preview area
        splitter.setSizes([self.width() * 0.66, self.width() * 0.33])

        # Add layouts to main layout
        main_layout.addWidget(splitter)
        main_layout.addLayout(preview_layout)
        main_layout.addLayout(search_layout)

        # Set layout for the widget
        self.setLayout(main_layout)

        self.setGeometry(100, 100, 800, 600)
