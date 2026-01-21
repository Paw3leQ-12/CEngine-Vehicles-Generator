from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSpinBox, QStackedWidget, QDoubleSpinBox, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.scripts.functions import load_setting
import json

class PLabeledSpinBox(QWidget):
    def __init__(self,
                 text: str,
                 minValue: int = 1,
                 maxValue: int = 100
                 ):
        # Setup

        super().__init__()
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)

        # Widgets

        label = QLabel(text)
        self.spinBox = QSpinBox(minimum=minValue, maximum=maxValue)

        # Modifiers

        self.spinBox.setFixedWidth(100)

        # Layout

        rootLayout.addWidget(label)
        rootLayout.addWidget(self.spinBox)

    def get(self):
        return self.spinBox.value()
    
    def set(self, value: int):
        self.spinBox.setValue(value)

    def on_change(self, function):
        self.spinBox.valueChanged.connect(function)

class PLabeledDoubleSpinBox(QWidget):
    def __init__(self,
                 text: str,
                 minValue: int = 0.0,
                 maxValue: int = 100.0,
                 step: float = 0.05
                 ):
        # Setup

        super().__init__()
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)

        # Widgets

        label = QLabel(text)
        self.spinBox = QDoubleSpinBox(minimum=minValue, maximum=maxValue, singleStep=step)

        # Modifiers

        self.spinBox.setFixedWidth(100)

        # Layout

        rootLayout.addWidget(label)
        rootLayout.addWidget(self.spinBox)

    def get(self):
        return self.spinBox.value()
    
    def set(self, value: int):
        self.spinBox.setValue(float(value))


class PLabeledLineEdit(QWidget):
    def __init__(self,
                 text: str):
        # Setup

        super().__init__()
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)

        # Widgets

        label = QLabel(text)
        self.lineEdit = QLineEdit()

        # Modifiers

        self.lineEdit.setFixedWidth(100)
        self.lineEdit.textChanged.connect(self.update_tool_tip)

        # Layout

        rootLayout.addWidget(label)
        rootLayout.addWidget(self.lineEdit)

    def get(self):
        return self.lineEdit.text()
    
    def set(self, text):
        self.lineEdit.setText(str(text))

    def update_tool_tip(self):
        self.lineEdit.setToolTip(self.get())

class PLabeledCheckBox(QWidget):
    def __init__(self,
                 text: str,
                 value = None,
                 state = False):
        # Setup

        self.value = value
        super().__init__()
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)

        # Widgets

        self.checkBox = QCheckBox(text)

        # Modifiers

        self.checkBox.setCursor(Qt.PointingHandCursor)

        # Layout

        rootLayout.addWidget(self.checkBox)

        self.set(state)

    def get(self):
        return self.checkBox.isChecked()
    
    def set(self, state: bool):
        self.checkBox.setChecked(state)

    def on_change(self, command):
        self.checkBox.toggled.connect(lambda: command(self.get(), self.value, self))

class PLabeledComboBox(QWidget):
    def __init__(self,
                 text: str,
                 values: list[str]
                 ):
        # Setup

        super().__init__()
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)

        # Widgets

        label = QLabel(text)
        self.comboBox = QComboBox()

        # Modifiers

        self.comboBox.setFixedWidth(100)
        self.comboBox.addItems(values)

        # Layout

        rootLayout.addWidget(label)
        rootLayout.addWidget(self.comboBox)

    def get(self):
        return self.comboBox.currentText()
    
    def on_change(self, function):
        self.comboBox.currentIndexChanged.connect(function)

    def current_index(self):
        return self.comboBox.currentIndex()
    
    def update_items(self, values):
        self.comboBox.clear()
        self.comboBox.addItems(values)

class PTopLevel(QWidget):
    def __init__(self, title: str = "Top Level"):
        # Setup

        super().__init__()
        self.rootLayout = QVBoxLayout()
        self.setLayout(self.rootLayout)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("src/ui/img/icon.ico"))

    def add_widget(self, widget):
        self.rootLayout.addWidget(widget)

class PSetting(QWidget):
    def __init__(self, name, widget, text: str = "Setting"):
        # Setup

        self.name = name
        super().__init__()
        self.rootLayout = QHBoxLayout()
        self.setLayout(self.rootLayout)
        
        # Widgets

        buttonApply = QPushButton("Apply")
        buttonRestore = QPushButton("Restore")
        self.widget = widget(text)

        # Signals

        buttonApply.clicked.connect(lambda: self.change_setting("apply"))
        buttonRestore.clicked.connect(lambda: self.change_setting("restore"))

        # Modifiers

        buttonApply.setFixedWidth(65)
        buttonRestore.setFixedWidth(65)

        # Layout

        self.rootLayout.addWidget(self.widget)
        self.rootLayout.addWidget(buttonApply)
        self.rootLayout.addWidget(buttonRestore)

        # Other

        self.widget.set(load_setting(name))

    def change_setting(self, mode: str):
        with open("src/data/settings.json", "r") as file:
            jsonData = json.load(file)

        if mode == "apply":
            jsonData[self.name]["user"] = self.widget.get()
        elif mode == "restore":
            jsonData[self.name]["user"] = False

        with open("src/data/settings.json", "w") as file:
            jsonData = json.dump(jsonData, file, indent=4)

        self.widget.set(load_setting(self.name))
    
class PStackedWidget(QStackedWidget):
    def __init__(self):
        # Setup

        super().__init__()
        self.widgets = []

    def add_widget(self, widget):
        self.addWidget(widget)
        self.widgets.append(widget)

    def get(self):
        data = []
        for widget in self.widgets:
            data.append(widget.get())
        return data

class PSeparator(QFrame):
    def __init__(self, mode: str = "vertical", property: str = False):
        # Setup

        super().__init__()
        if mode == "vertical":
            self.setFrameShape(QFrame.VLine)
        elif mode == "horizontal":
            self.setFrameShape(QFrame.HLine)

        if property:
            self.setProperty("class", property)