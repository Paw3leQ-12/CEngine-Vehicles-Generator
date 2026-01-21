English | [Polski](README.pl.md)

![Status](https://img.shields.io/badge/Status-BETA-red?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

# CEngine Vehicles Generator (v0.1.0)

CEngine Vehicles Generator is a tool for generating `.prefab` files for the **CEngine** game engine developed by Techland.  
The application is written in Python and is designed to work with the version of the engine used to create *Dying Light 2*.

This tool reduces the hard and repetitive work of placing vehicles on community maps.  
It allows you to generate vehicles in many different models (not all yet), change vehicle textures, and control how vehicles are placed on the map.

## Authors

- [@Paw3leQ](https://github.com/Paw3leQ-12)

## Features

- Generate only selected vehicles  
- Enable and disable textures for each vehicle  
- Change spacing parameters  
- Change vehicle proportions  
- Add your own `.prefab` files as decorations  

## Installation

1. Download the GitHub repository  
2. Extract the `.zip` file on your computer  
3. Run `generator.exe` located in the main folder  

## Documentation

### Main window

After running the executable file (`generator.exe`), you will see the main application window.  
Below is a detailed description of the interface to help you use the program. We start from the left side.

1. On the far left, there is the main form. You must fill in all fields for the program to work correctly. Below is a description of each option:
    - **Files directory** - sets the default path where generated files will be saved.  
      It is recommended to use the path to your *Dying Light 2* project, specifically the *Prefabs* folder that contains all `.prefab` files.
    - **File name** - name of the generated file that will contain all generated vehicles.
    - **Vehicles amount** - number of vehicles to generate.
    - **Min spacing** - minimum distance from the previous vehicle.
    - **Max spacing** - maximum distance from the previous vehicle.
    - **Displacement** - Moves cars left and right.
    - **Auto-gen prefix** - prefix name for automatically generated `.prefab` files that are not the main file.  
      These are single-vehicle prefab files created to build the correct hierarchy.
    - **Generate trunks** - Turned on by default. It says if program should generate trunks for vehicles
    - **Generate decorations** - It is responsible for generating decorations (your own `..prefab` files). Turned on by default.
    - **Preset** - allows you to load predefined generator settings (vehicle models and skins).

2. The second section contains vehicle model selection.  
   Select the checkboxes to include specific models in generation.

3. The third section is for texture selection.  
   By default, all textures are enabled.  
   Textures are changed per vehicle, which you can select using the dropdown list at the top.

4. The fourth section is used to set vehicle proportions relative to each other.  
   This list updates automatically when a vehicle model is enabled or disabled.

5. At the top, there is a small menu bar with one **File** tab that contains two options:
    - **Close app** – closes the application.
    - **Settings** – opens the settings window described below.

6. The settings window allows you to save settings so they load automatically when the application starts.  
   Keep in mind that every change requires restarting the application because the main interface does not refresh automatically.  
   You can change:
    - file save path,
    - generated prefix,
    - minimum spacing,
    - maximum spacing.


7. The previously mentioned menu bar also contains the **Preset** tab, which offers two options:
   - **Create preset** - creates a new preset that can be loaded.
   - **Delete preset** - deletes the selected preset.

   It is worth remembering that when creating a preset, you only need to provide its name, and the inserted data will reflect the state of the current generator settings.

### Adding custom decorations

To add decorations, you must have the **CEngine** installed.  
Follow these steps:

1. Open CEngine  
2. Open any project  
3. Place the `.msh` vehicle file for which you are creating decorations, for example `veh_sedan_a.msh`  
4. Place decorations around the `.msh` file in any way you like  
5. Save the decorations (without the `.msh` model) into one `.prefab` file with any name  
6. Copy the vehicle model position  
7. Open the created `.prefab` file and select *Edit pivot*  
8. Go to the *Attributes* tab and paste the copied vehicle position  
9. Save the changes  
10. Move the file to the correct folder located in `\src\data\decorations` inside the extracted `.zip`  

You can add any number of decorations.  
Decorations will be randomly selected for each vehicle, or no decoration may be selected.

## FAQ

**Question:** How long do you plan to support this project?  
**Answer:** This project is part of a larger idea that aims to make *Dying Light 2* map creation much faster and easier, so support will not end anytime soon.

**Question:** What will future updates focus on and when can we expect them?  
**Answer:** Future updates will focus mainly on adding missing vehicle models, more configuration options, UI improvements, and *Quality of Life* changes. Release dates are not fixed.

**Question:** Is this everything you plan to add?  
**Answer:** Absolutely not. There are many more features planned, including full street grid generation with vehicles, but this is a long-term goal.

**Question:** How can I send you an idea or suggestion?  
**Answer:** Add me on Discord: `paw3leq_`.

**Question:** Can I edit the code and redistribute it?  
**Answer:** In short: yes, but you must credit the original author (me).  
For full details, please check the [License](LICENSE.md).
