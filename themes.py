from PySide6.QtWidgets import QApplication

class Theme:
    def __init__(self):
        self.primary_color = "#ffffff"  # Set primary color to white
        self.secondary_color = "#cccccc"
        self.font_family = "Arial"
        self.font_size = "14px"

    def get_style_sheet(self) -> str:
        return (f"color: black;"  # Set text color to black
                f" background-color: {self.secondary_color};"
                f" font-family: {self.font_family};"
                f" font-size: {self.font_size};")


class ForestGreen(Theme):
    def __init__(self):
        super().__init__()
        self.primary_color = "#228B22"  # Forest green
        self.secondary_color = "#32CD32"  # Lime green


class SkyBlue(Theme):
    def __init__(self):
        super().__init__()
        self.primary_color = "#87CEEB"  # Sky blue
        self.secondary_color = "#00BFFF"  # Deep sky blue


class Sand(Theme):
    def __init__(self):
        super().__init__()
        self.primary_color = "#ffffff"  # Set primary color to white
        self.secondary_color = "#EEE8AA"  # Pale goldenrod