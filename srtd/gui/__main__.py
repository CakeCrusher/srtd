from .file_explorer import FileExplorer
from .themes import *
from PySide6.QtWidgets import (
    QApplication,
)

def launch_gui():
    app = QApplication([])
    window = FileExplorer(app, PastelYellow())
    window.show()
    app.exec()

if __name__ == "__main__":
    launch_gui()
