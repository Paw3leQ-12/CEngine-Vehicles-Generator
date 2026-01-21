from src.scripts.ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication([])

with open("src/ui/style.qss", "r") as file:
    app.setStyleSheet(file.read())

mainWindow = MainWindow()
mainWindow.show()

app.exec()
