from PySide6.QtWidgets import QApplication

from PySide6.QtWidgets import QApplication


class Theme:
    def __init__(self, app: QApplication):
        self.app = app
        self.primary_color = "#ffffff"
        self.secondary_color = "#cccccc"
        self.text_color = "#000000"
        self.font_family = "Arial"
        self.font_size = "14px"

    def get_stylesheet_for(self, widget_type: str) -> str:
        """Return a stylesheet string for the given widget type."""
        styles = {
            "QTreeView": f"""
                QTreeView {{
                    background-color: {self.secondary_color};
                    color: {self.text_color};
                    border: 1px solid {self.text_color};
                    font-family: {self.font_family};
                    font-size: {self.font_size};
                }}
            """,
            "QLineEdit": f"""
                QLineEdit {{
                    background-color: {self.primary_color};
                    color: {self.text_color};
                    border: 1px solid {self.text_color};
                    padding: 4px;
                    font-family: {self.font_family};
                    font-size: {self.font_size};
                }}
            """,
            "QPushButton": f"""
                QPushButton {{
                    background-color: {self.secondary_color};
                    color: {self.text_color};
                    border: 1px solid {self.text_color};
                    border-radius: 5px;
                    padding: 6px;
                    font-family: {self.font_family};
                    font-size: {self.font_size};
                }}
                QPushButton:hover {{
                    background-color: {self.text_color};
                    color: {self.primary_color};
                }}
            """,
            "QLabel": f"""
                QLabel {{
                    color: {self.text_color};
                    font-family: {self.font_family};
                    font-size: {self.font_size};
                }}
            """
        }
        return styles.get(widget_type, "")

    def apply_theme(self):
        """Optionally set a global stylesheet for the app."""
        self.app.setStyleSheet(f"""
            QWidget {{
                background-color: {self.primary_color};
                color: {self.text_color};
                font-family: {self.font_family};
                font-size: {self.font_size};
            }}
        """)


class ForestGreen(Theme):
    def __init__(self, app):
        super().__init__(app)
        self.primary_color = "#228B22"  # Forest green
        self.secondary_color = "#32CD32"  # Lime green
        self.apply_theme()

class SkyBlue(Theme):
    def __init__(self, app):
        super().__init__(app)
        self.primary_color = "#87CEEB"  # Sky blue
        self.secondary_color = "#00BFFF"  # Deep sky blue
        self.apply_theme()

class Sand(Theme):
    def __init__(self, app):
        super().__init__(app)
        self.primary_color = "#F5F5DC"  # Beige
        self.secondary_color = "#EEE8AA"  # Pale goldenrod
        self.apply_theme()