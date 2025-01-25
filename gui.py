from file_explorer import FileExplorer
from themes.theme import Theme
from PySide6.QtWidgets import (
    QApplication,
)

if __name__ == "__main__":
    app = QApplication([])
    window = FileExplorer(Theme(app, "forest_green"))
    window.show()
    app.exec()