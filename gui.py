from file_explorer import FileExplorer
from themes import *
from PySide6.QtWidgets import (
    QApplication,
)

if __name__ == "__main__":
    app = QApplication([])
    window = FileExplorer(app, Sand())
    window.show()
    app.exec()