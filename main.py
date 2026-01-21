from src.scripts.ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

app = QApplication([])

apply_stylesheet(app, "dark_red.xml")

mainWindow = MainWindow()
mainWindow.show()

app.exec()
