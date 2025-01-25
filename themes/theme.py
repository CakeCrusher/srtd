from PySide6.QtWidgets import QApplication

class Theme:
    app: QApplication = None
    primary_color: str = None
    secondary_color: str  = None

    def __init__(self, app, theme_name: str = None):
        __app = app
        if theme_name == "forest_green":
            self.primary_color = "#228B22"
            self.secondary_color = "#32CD32"
        elif theme_name == "sky_blue":
            self.primary_color = "#87CEEB"
            self.secondary_color = "#00BFFF"
        elif theme_name == "sand":
            self.primary_color = "#F5F5DC"
            self.secondary_color = "#EEE8AA"

    def apply_theme(self) -> None:
        if self.primary_color is None or self.secondary_color is None:
            return
        self.app.setStyleSheet(f"""
            QWidget {{
                background-color: {self.primary_color};
            }}
        """)