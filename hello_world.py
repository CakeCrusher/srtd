import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    # Load QML file
    engine.load("main.qml")  # Ensure the path to main.qml is correct

    if not engine.rootObjects():
        print("Error: Could not start application.")
        sys.exit(-1)

    print("Application started.")
    exit_code = app.exec()  # Start the event loop
    sys.exit(exit_code)
