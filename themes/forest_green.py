from PySide6.QtWidgets import QApplication

from theme import Theme

class ForestGreen(Theme):
    def __init__(self, app: QApplication):
        self.__primary_color = "#d1e7cc"
        self.__secondary_color = "#62ad52"
        super().__init__(app)
