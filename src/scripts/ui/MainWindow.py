from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QGridLayout, QInputDialog, QLabel, QScrollArea, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QCoreApplication
from src.scripts.ui.PComponents import PLabeledLineEdit, PLabeledSpinBox, PTopLevel, PSetting, PStackedWidget, PLabeledCheckBox, PLabeledComboBox, PLabeledDoubleSpinBox, PSeparator
from src.scripts.functions import get_position, generate_vehicle_preset, load_setting
import os
from random import choice, uniform
import json

class MainWindow(QMainWindow):
    def __init__(self):
        # Setup

        super().__init__()

        self.setWindowTitle("CEngine Vehicles Generator by Paw3leQ")
        self.setMinimumSize(1500, 700)
        self.setWindowIcon(QIcon("src/ui/img/icon.ico"))

        # Actions

        fileClose = QAction("Close app", self)
        fileSettings = QAction("Settings", self)

        presetCreate = QAction("Create preset", self)
        presetDelete = QAction("Delete preset", self)

        # Widgets:
        
        self.form = Form()

        # Menu bar

        menuBar = self.menuBar()
        menuFile = menuBar.addMenu("File")
        menuFile.addAction(fileClose)
        menuFile.addAction(fileSettings)
        menuPreset = menuBar.addMenu("Preset")
        menuPreset.addAction(presetCreate)
        menuPreset.addAction(presetDelete)
        
        # Settings window

        self.settingDirectory = PSetting("directory", PLabeledLineEdit, "Destination path: ")
        self.settingAutoGenPrefix = PSetting("prefix", PLabeledLineEdit, "Auto-gen prefix: ")
        self.settingMinSpacing = PSetting("minSpacing", PLabeledDoubleSpinBox, "Min spacing: ")
        self.settingMaxSpacing = PSetting("maxSpacing", PLabeledDoubleSpinBox, "Max spacing: ")
        self.settingDisplacement = PSetting("displacement", PLabeledDoubleSpinBox, "Displacement: ")

        self.windowSettings = PTopLevel("Default settings")

        self.windowSettings.add_widget(self.settingDirectory)
        self.windowSettings.add_widget(self.settingAutoGenPrefix)
        self.windowSettings.add_widget(self.settingMinSpacing)
        self.windowSettings.add_widget(self.settingMaxSpacing)
        self.windowSettings.add_widget(self.settingDisplacement)
        self.windowSettings.add_widget(QLabel("IMPORTANT NOTE: Changes take effect immediately, but fields in main window may not update visually. For best results, restart the application after changing these options.", wordWrap=True))

        # Modifiers

        fileClose.triggered.connect(self.destroy_app)
        fileSettings.triggered.connect(self.windowSettings.show)
        presetCreate.triggered.connect(self.create_preset)
        presetDelete.triggered.connect(self.delete_preset)

        # Addiional 

        self.setCentralWidget(self.form)
        
    def destroy_app(self):
        QCoreApplication.quit()

    def create_preset(self):
        text, ok = QInputDialog.getText(self, "Preset name", "Enter name of your preset:")
        if ok:
            with open("src/ui/ui_data.json", "r") as file:
                fileData = json.load(file)
            for preset in fileData["presets"]:
                if preset["label"] == text:
                    QMessageBox.warning(self, "Unable to create preset", "Preset with this name already exist!")
                    return

            preset = self.form.create_preset(text)
            fileData["presets"].append(preset)
            with open("src/ui/ui_data.json", "w") as file:
                fileData = json.dump(fileData, file, indent=4)
            self.form.update_combo_box()
            QMessageBox.information(self, "Preset created", f"Preset {text} created.")
            

    def delete_preset(self):
        text, ok = QInputDialog.getText(self, "Preset name", "Enter name of your preset:")
        if ok:
            with open("src/ui/ui_data.json", "r") as file:
                fileData = json.load(file)
            for preset in fileData["presets"]:
                if preset["label"] == text:
                    fileData["presets"].remove(preset)
                    QMessageBox.information(self, "Preset deleted", f"Preset {text} deleted.")
                    break
            with open("src/ui/ui_data.json", "w") as file:
                fileData = json.dump(fileData, file, indent=4)
            self.form.update_combo_box()

class Form(QWidget):
    def __init__(self):
        # Setup

        super().__init__()

        rootLayout = QHBoxLayout()
        self.skinsLayout = QVBoxLayout()
        mainFormLayout = QVBoxLayout()
        carsCheckBoxLayout = QGridLayout()
        rightSideContainerLayout = QHBoxLayout()
        self.vehiclesProportionLayout = QVBoxLayout()

        self.setLayout(rootLayout)
        
        self.vehiclesTypes = []
        self.checkBoxes = []
        self.checkBoxesSkins = {}
        allTypes = []
        self.activeSkins = {}
        self.activeVehiclesWidgets = {}
        self.total = 0
        row = 0
        column = 0

        with open("src/ui/ui_data.json", "r") as file:
            UIData = json.load(file)

        with open("src/data/veh_data.json", "r") as file:
            vehData = json.load(file)
    
        # Widgets 
        
        self.stack = PStackedWidget()
        self.vehiclesProportionWidget = QWidget()
        self.vehiclesProportionScroll = QScrollArea(widgetResizable=True)
        generateButton = QPushButton("Generate")
        self.directory = PLabeledLineEdit("Files directory:")
        self.fileName = PLabeledLineEdit("File name:")
        self.maxSpacing = PLabeledDoubleSpinBox("Max spacing:")
        self.minSpacing = PLabeledDoubleSpinBox("Min spacing:")
        self.displacement = PLabeledDoubleSpinBox("Displacement:")
        self.vehiclesAmount = PLabeledSpinBox("Vehicles amount:")
        self.prefix = PLabeledLineEdit("Auto-gen prefix:")
        self.generateTrunks = PLabeledCheckBox("Generate trunks", state=True)
        self.generateDecorations = PLabeledCheckBox("Generate decorations", state=True)

        for key, data in vehData.items():
            self.activeSkins[key] = []
            self.checkBoxesSkins[key] = []
            mainWidget = QWidget()
            layout = QVBoxLayout(mainWidget)
            for skin in data["skins"]:
                widget = PLabeledCheckBox(skin, skin, state = True)
                layout.addWidget(widget)
                widget.on_change(self.skin_changed)
                self.activeSkins[key].append(skin)
                self.checkBoxesSkins[key].append(widget)
            allTypes.append(key)
            self.stack.add_widget(mainWidget)

        self.preset = PLabeledComboBox("Load preset:", self.load_presets())
        self.comboBoxModels = PLabeledComboBox("Model: ", allTypes)


        # Modifiers

        generateButton.clicked.connect(self.generate_vehicles)
        self.comboBoxModels.on_change(self.change_stack)
        self.preset.on_change(self.load_preset)

        # Layout

        rootLayout.addLayout(mainFormLayout)
        rootLayout.addWidget(PSeparator("vertical", "separator"))
        rootLayout.addLayout(carsCheckBoxLayout)
        rootLayout.addWidget(PSeparator("vertical", "separator"))
        rootLayout.addLayout(rightSideContainerLayout)
        mainFormLayout.addWidget(self.directory)
        mainFormLayout.addWidget(self.fileName)
        mainFormLayout.addWidget(self.vehiclesAmount)
        mainFormLayout.addWidget(self.minSpacing)
        mainFormLayout.addWidget(self.maxSpacing)
        mainFormLayout.addWidget(self.displacement)
        mainFormLayout.addWidget(self.prefix)
        mainFormLayout.addWidget(self.generateTrunks)
        mainFormLayout.addWidget(self.generateDecorations)
        mainFormLayout.addWidget(self.preset)
        mainFormLayout.addWidget(generateButton)
        rightSideContainerLayout.addLayout(self.skinsLayout)
        rightSideContainerLayout.addWidget(PSeparator("vertical", "separator"))
        rightSideContainerLayout.addWidget(self.vehiclesProportionScroll)
        self.skinsLayout.addWidget(QLabel("Mesh skins:"))
        self.skinsLayout.addWidget(self.comboBoxModels)
        self.skinsLayout.addWidget(self.stack)
        self.vehiclesProportionLayout.addWidget(QLabel("Proportions:"))

        for checkBoxData in UIData["checkBoxes"]:
            checkBox = PLabeledCheckBox(checkBoxData["label"], checkBoxData["value"])
            checkBox.on_change(self.type_changed)
            carsCheckBoxLayout.addWidget(checkBox, row, column)
            column += 1
            if column % 2 == 0:
                row += 1
                column = 0
            self.checkBoxes.append(checkBox)

        # Additional

        self.vehiclesProportionWidget.setLayout(self.vehiclesProportionLayout)
        self.vehiclesProportionScroll.setWidget(self.vehiclesProportionWidget)

        self.skinsLayout.addStretch()
        self.vehiclesProportionLayout.addStretch()

        self.load_settings()

    def load_presets(self):
        presetsList = []
        with open("src/ui/ui_data.json", "r") as file:
            UIData = json.load(file)
        for preset in UIData["presets"]:
            presetsList.append(preset["label"])

        return presetsList

    def update_combo_box(self):
         self.preset.update_items(self.load_presets())

    def create_preset(self, name):
        preset = {}
        preset["label"] = name
        preset["values"] = []
        preset["disabledSkins"] = {}
        for checkBox in self.checkBoxes:
            if checkBox.get():
                preset["values"].append(checkBox.value)
        for model, checkBoxes in self.checkBoxesSkins.items():
            for checkBox in checkBoxes:
                if not checkBox.get():
                    if model not in preset["disabledSkins"].keys():
                        preset["disabledSkins"][model] = []
                    preset["disabledSkins"][model].append(checkBox.value)
        return preset


    def one_in_changed(self):
        self.total = 0
        for widget in self.activeVehiclesWidgets:
            self.total += self.activeVehiclesWidgets[widget].get()
        for widget in self.activeVehiclesWidgets:
            self.activeVehiclesWidgets[widget].change_text(f"{self.activeVehiclesWidgets[widget].get()} in {self.total}")

    def change_stack(self):
        self.stack.setCurrentIndex(self.comboBoxModels.current_index())

    def skin_changed(self, state, type, widget):
        for model, checkBoxesSkin in self.checkBoxesSkins.items():
            for checkBoxSkin in checkBoxesSkin:
                if checkBoxSkin == widget:
                    skins = self.activeSkins[model]
                    if state:
                        if type not in skins:
                            skins.append(type)
                    else:
                        if type in skins:
                            skins.remove(type)

    def load_preset(self):
        for checkBox in self.checkBoxes:
            checkBox.set(False)
        for checkBoxesSkin in self.checkBoxesSkins.values():
            for checkBoxSkin in checkBoxesSkin:
                checkBoxSkin.set(True)
        with open("src/ui/ui_data.json", "r") as file:
            fileData = json.load(file)
        for preset in fileData["presets"]:
            if preset["label"] == self.preset.get():
                for checkBox in self.checkBoxes:
                    if checkBox.value in preset["values"]:
                        checkBox.set(True)
                for modelName, disabledSkins in preset["disabledSkins"].items():
                    for checkBox in self.checkBoxesSkins[modelName]:
                        if checkBox.value in disabledSkins:
                            checkBox.set(False)

    def type_changed(self, state, type, w):
        if state:
            self.vehiclesTypes.append(type)
            widget = OneIn(type, self.total)
            self.vehiclesProportionLayout.addWidget(widget)
            self.activeVehiclesWidgets[type] = widget
            self.vehiclesProportionLayout.addWidget(widget)
        else:
            self.vehiclesTypes.remove(type)
            widget = self.activeVehiclesWidgets[type]
            self.vehiclesProportionLayout.removeWidget(widget)
            widget.deleteLater()
            del self.activeVehiclesWidgets[type]
        for widget in self.activeVehiclesWidgets:
            self.activeVehiclesWidgets[widget].on_change(self.one_in_changed)
        self.one_in_changed()
        

    def load_settings(self):
        self.directory.set(load_setting("directory"))
        self.prefix.set(load_setting("prefix"))
        self.minSpacing.set(load_setting("minSpacing"))
        self.maxSpacing.set(load_setting("maxSpacing"))
        self.displacement.set(load_setting("displacement"))

    def generate_vehicles(self):
        vehicles = self.vehiclesAmount.get()
        prefabName = self.fileName.get()

        fileData = {
            "__filename__": {
                "Version": 4,
                "RuntimeData": {
                    "Components": []
                },
                "PrefabEditorData": {
                    "DataVersion": "2"
                }
            }
        }

        vehiclePositionZ = 0.0
        previousVehicle = False
        vehiclesList = []
            
        for widget in self.activeVehiclesWidgets:
            for i in range(self.activeVehiclesWidgets[widget].get()):
                vehiclesList.append(self.activeVehiclesWidgets[widget].text)

        for i in range(vehicles):

            vehicle = choice(vehiclesList)

            vehicleRotateY = uniform(-5.0, 5.0)
            vehiclePositionNoiseZ = uniform(self.minSpacing.get(), self.maxSpacing.get())
            vehiclePositionX = uniform(-self.displacement.get(), self.displacement.get())

            if previousVehicle:
                vehiclePositionZ += get_position(vehicle, previousVehicle)

            fileData["__filename__"]["RuntimeData"]["Components"].append({
                "Class": "CEntity",
                "PrefabFieldsNative": {
                    "m_PcId": [6, i],
                    "m_PrefabName": [12, generate_vehicle_preset(vehicle, self.directory.get(), self.activeSkins, self.generateTrunks.get())],
                    "m_Rotate": [14, [-0.0, vehicleRotateY, -0.0]],
                    "m_Translate": [14, [vehiclePositionX, 0.0, vehiclePositionZ + vehiclePositionNoiseZ]]
                }
            })

            if self.generateDecorations.get():
                decorations = [False]
                for file in os.listdir(f"src/data/decorations/{vehicle}"):
                    decorations.append(file[:-7])

                addon = choice(decorations)
                if addon:
                    fileData["__filename__"]["RuntimeData"]["Components"].append({
                    "Class": "CEntity",
                    "PrefabFieldsNative": {
                        "m_PcId": [6, i],
                        "m_PrefabName": [12, addon],
                        "m_Rotate": [14, [-0.0, vehicleRotateY, -0.0]],
                        "m_Translate": [14, [vehiclePositionX, 0.0, vehiclePositionZ + vehiclePositionNoiseZ]]
                    }
                })

            vehiclePositionZ += vehiclePositionNoiseZ
            previousVehicle = vehicle

        with open(f"{self.directory.get()}/{prefabName}.prefab", "w") as prefab:
            json.dump(fileData, prefab, indent=2)

class OneIn(QWidget):
    def __init__(self, text, variable):
        super().__init__()
        self.text = text
        self.variable = variable
        rootLayout = QHBoxLayout()
        self.setLayout(rootLayout)
        self.spinBox = PLabeledSpinBox(text)
        self.label = QLabel()

        rootLayout.addWidget(self.spinBox)
        rootLayout.addWidget(self.label)

    def on_change(self, command):
        self.spinBox.on_change(command)

    def get(self):
        return self.spinBox.get()
    
    def change_text(self, text):
        self.label.setText(text)
    