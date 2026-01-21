from random import choice, randint
import json

def choose_skin(vehicle, activeSkins):
    with open("src/data/veh_data.json", "r") as file:
        jsonData = json.load(file)
    skins = jsonData[vehicle]["skins"]
    brokenSkins = []
    if jsonData[vehicle]["skinsBrokenGlass"]:
        for skin in skins:
            brokenSkins.append(f"{skin}_broken_glass")
    for brokenSkin in brokenSkins:
            skins.append(brokenSkin)
    skin = choice(skins)
    while skin not in activeSkins[vehicle]:
        skin = choice(skins)
    return skin

def get_vehicle_data(vehicle):
    data = {}
    with open("src/data/veh_data.json", "r") as file:
        jsonData = json.load(file)
    data["hitbox"] = jsonData[vehicle]["hitbox"]
    data["meshName"] = jsonData[vehicle]["meshName"]
    data["trunks"] = jsonData[vehicle]["trunks"]
    return data

def get_position(vehicle, previousVehicle):
    with open("src/data/veh_data.json", "r") as file:
        jsonData = json.load(file)
    return jsonData[vehicle]["moves"][previousVehicle]

def generate_vehicle_preset(vehicle, directory, activeSkins, generateTrunks):
    vehicleData = get_vehicle_data(vehicle)
    vehicleSkin = choose_skin(vehicle, activeSkins)
    fileData = {
            "__filename__": {
                    "Version": 4,
                    "RuntimeData": {
                        "Components": []
                    },
                    "PrefabEditorData" : {
                        "DataVersion" : "2"
                    }
                }
            }
    
    fileData["__filename__"]["RuntimeData"]["Components"].append({
          "Class": "CEntity",
          "PrefabFieldsNative": {
            "m_EntityComponentsExtents": [69, vehicleData["hitbox"]],
            "m_PcId": [6, 1],
            "m_PrefabName": [12, "mesh"],
            "m_PresetNames": [12, f"Meshes;{vehicleData["meshName"]}"],
            "m_Translate": [14, [0.0, 0.0, 0.0]]
          },
          "Fields": {
            "SkinName": vehicleSkin
          }
        })
    
    if vehicleSkin in ["Taxi", "Taxi_broken_glass", "Police", "Police_broken_glass"]:
        if vehicleSkin in ["Taxi", "Taxi_broken_glass"]:
            addonHitbox = [-0.0117805, 0.7713758, -0.2871828, 0.9233202, 0.7713758, 0.5512479]
            addonMesh = "veh_sedan_taxi_addon"
        elif vehicleSkin in ["Police", "Police_broken_glass"]:
            addonHitbox = [-0.0135607, 0.763553, 0.4688069, 0.8897193, 0.763553, 1.582854]
            addonMesh = "veh_sedan_police_addon"
        fileData["__filename__"]["RuntimeData"]["Components"].append({
          "Class": "CEntity",
          "PrefabFieldsNative": {
            "m_EntityComponentsExtents": [69, addonHitbox],
            "m_PcId": [6, 2],
            "m_PrefabName": [12, "mesh"],
            "m_PresetNames": [12, f"Meshes;{addonMesh}"],
            "m_Translate": [14, [0.0, 0.0, 0.0]]
          }
        })

    if vehicleData["trunks"] and generateTrunks:
        position = choice(vehicleData["trunks"]["positions"])
        if position:
            trunkRotationX = position["trunkRotationX"]
            trunkRotationY = position["trunkRotationY"]
            trunkPositionY = position["trunkPositionY"]
            trunkPositionZ = position["trunkPositionZ"]
            fileData["__filename__"]["RuntimeData"]["Components"].append({
            "Class": "CEntity",
            "PrefabFieldsNative": {
                "m_EntityComponentsExtents": [69, vehicleData["trunks"]["hitbox"]],
                "m_PcId": [6, 3],
                "m_PrefabName": [12, "mesh"],
                "m_PresetNames": [12, f"Meshes;{vehicleData["trunks"]["mesh"]}"],
                "m_Rotate": [14, [trunkRotationX, trunkRotationY, 0.0]],
                "m_Translate": [14, [0.0, trunkPositionY, trunkPositionZ]]
            },
            "Fields": {
                "SkinName": vehicleSkin
            }
            })
        else:
            position = {}
            position["index"] = 0
    else:
        position = {}
        position["index"] = 0

    fileName = f"{load_setting("prefix")}_{vehicleData["meshName"]}_{vehicleSkin}_{position["index"]}"

    with open(f"{directory}/{fileName}.prefab", "w") as prefab:
        json.dump(fileData, prefab, indent=2)
    
    return fileName

def load_setting(setting: str):
    with open("src/data/settings.json", "r") as file:
        jsonData = json.load(file)

    if jsonData[setting]["user"]:
        return jsonData[setting]["user"]
    else:
        return jsonData[setting]["default"]