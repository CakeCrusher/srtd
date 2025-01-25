from file_explorer import FileExplorer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

if __name__ == "__main__":
    app = QApplication([])
    window = FileExplorer()
    window.show()
    app.exec()