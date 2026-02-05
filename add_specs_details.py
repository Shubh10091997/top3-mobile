import json
import os

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "data", "data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Phone specs database
phone_specs = {
    "Redmi A2": {"ram": "3GB", "processor": "MediaTek Helio G35", "storage": "32GB", "main_camera": "8MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Tecno Spark Go 2024": {"ram": "4GB", "processor": "MediaTek Helio G35", "storage": "64GB", "main_camera": "8MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Infinix Smart 8": {"ram": "4GB", "processor": "MediaTek Helio G35", "storage": "64GB", "main_camera": "8MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Samsung Galaxy F04": {"ram": "4GB", "processor": "MediaTek Exynos 850", "storage": "64GB", "main_camera": "13MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Lava Blaze 2": {"ram": "4GB", "processor": "MediaTek Helio G35", "storage": "64GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Redmi 13C": {"ram": "4GB", "processor": "MediaTek Helio G85", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Samsung F14": {"ram": "4GB", "processor": "Samsung Exynos 850", "storage": "64GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "6000mAh"},
    "Realme C55": {"ram": "4GB", "processor": "Snapdragon 680", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Redmi 12 5G": {"ram": "4GB", "processor": "Snapdragon 4 Gen 1", "storage": "128GB", "main_camera": "50MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Samsung Galaxy M14 5G": {"ram": "4GB", "processor": "Snapdragon 680", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "6000mAh"},
    "Realme Narzo 60x": {"ram": "4GB", "processor": "Snapdragon 680", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "iQOO Z6 Lite": {"ram": "4GB", "processor": "Snapdragon 680", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Samsung Galaxy F23": {"ram": "6GB", "processor": "Snapdragon 750G", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Redmi Note 12": {"ram": "4GB", "processor": "Snapdragon 685", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "iQOO Z7": {"ram": "6GB", "processor": "Snapdragon 782G", "storage": "128GB", "main_camera": "50MP", "front_camera": "16MP", "battery": "5000mAh"},
    "Redmi Note 12 Pro": {"ram": "6GB", "processor": "Snapdragon 685", "storage": "128GB", "main_camera": "108MP", "front_camera": "16MP", "battery": "5000mAh"},
    "Samsung Galaxy M34": {"ram": "6GB", "processor": "MediaTek Helio G99", "storage": "128GB", "main_camera": "50MP", "front_camera": "13MP", "battery": "6000mAh"},
    "iPhone 14 Pro": {"ram": "6GB", "processor": "Apple A16 Bionic", "storage": "256GB", "main_camera": "48MP", "front_camera": "12MP", "battery": "3200mAh"},
    "Samsung Galaxy S24": {"ram": "8GB", "processor": "Snapdragon 8 Gen 3", "storage": "256GB", "main_camera": "50MP", "front_camera": "12MP", "battery": "4000mAh"},
    "OnePlus 12": {"ram": "8GB", "processor": "Snapdragon 8 Gen 3", "storage": "256GB", "main_camera": "50MP", "front_camera": "16MP", "battery": "5400mAh"},
    "Realme GT 5 Pro": {"ram": "8GB", "processor": "Snapdragon 8 Gen 3", "storage": "256GB", "main_camera": "50MP", "front_camera": "16MP", "battery": "5400mAh"},
    "Samsung Galaxy S23 FE": {"ram": "8GB", "processor": "Snapdragon 8 Gen 1", "storage": "256GB", "main_camera": "50MP", "front_camera": "32MP", "battery": "4500mAh"},
    "Poco F5 Pro": {"ram": "8GB", "processor": "Snapdragon 8+ Gen 1", "storage": "256GB", "main_camera": "64MP", "front_camera": "20MP", "battery": "5160mAh"},
    "Realme 11 Pro Plus": {"ram": "8GB", "processor": "Snapdragon 7 Gen 1", "storage": "256GB", "main_camera": "50MP", "front_camera": "32MP", "battery": "5000mAh"},
    "OnePlus Nord CE 3": {"ram": "8GB", "processor": "Snapdragon 695", "storage": "128GB", "main_camera": "50MP", "front_camera": "16MP", "battery": "5000mAh"},
    "Samsung Galaxy A54": {"ram": "6GB", "processor": "Exynos 1280", "storage": "128GB", "main_camera": "50MP", "front_camera": "32MP", "battery": "5000mAh"},
    "Poco X5 Pro": {"ram": "6GB", "processor": "Snapdragon 778G+", "storage": "128GB", "main_camera": "108MP", "front_camera": "16MP", "battery": "5000mAh"},
    "Redmi Note 13 Pro Plus": {"ram": "8GB", "processor": "Snapdragon 7 Gen 1", "storage": "256GB", "main_camera": "200MP", "front_camera": "16MP", "battery": "5000mAh"},
    "Realme 11x 5G": {"ram": "6GB", "processor": "Snapdragon 695", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Samsung Galaxy A34": {"ram": "6GB", "processor": "MediaTek Helio G80", "storage": "128GB", "main_camera": "50MP", "front_camera": "13MP", "battery": "5000mAh"},
    "Poco M6 Pro": {"ram": "4GB", "processor": "MediaTek Helio G99", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Redmi Note 13": {"ram": "4GB", "processor": "Snapdragon 685", "storage": "128GB", "main_camera": "108MP", "front_camera": "13MP", "battery": "5000mAh"},
    "Realme C67": {"ram": "4GB", "processor": "Snapdragon 680", "storage": "128GB", "main_camera": "50MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Poco M5": {"ram": "4GB", "processor": "MediaTek Helio G99", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Samsung Galaxy M14": {"ram": "4GB", "processor": "MediaTek Helio G80", "storage": "128GB", "main_camera": "50MP", "front_camera": "8MP", "battery": "5000mAh"},
    "Redmi A3": {"ram": "3GB", "processor": "MediaTek Helio G35", "storage": "32GB", "main_camera": "8MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Realme C51": {"ram": "3GB", "processor": "Snapdragon 680", "storage": "64GB", "main_camera": "8MP", "front_camera": "5MP", "battery": "5000mAh"},
    "Infinix Hot 30": {"ram": "4GB", "processor": "MediaTek Helio G88", "storage": "64GB", "main_camera": "13MP", "front_camera": "8MP", "battery": "6000mAh"},
}

# Add specs to all phones
for category in ["mobiles", "bikes"]:
    for phone in data.get(category, []):
        phone_name = phone.get("name", "")
        if phone_name in phone_specs:
            specs = phone_specs[phone_name]
            phone["ram"] = specs.get("ram", "4GB")
            phone["processor"] = specs.get("processor", "Unknown")
            phone["storage"] = specs.get("storage", "64GB")
            phone["main_camera"] = specs.get("main_camera", "50MP")
            phone["front_camera"] = specs.get("front_camera", "8MP")
            phone["battery"] = specs.get("battery", "5000mAh")
        else:
            # Add default specs if not found
            phone["ram"] = phone.get("ram", "4GB")
            phone["processor"] = phone.get("processor", "MediaTek Helio G85")
            phone["storage"] = phone.get("storage", "128GB")
            phone["main_camera"] = phone.get("main_camera", "50MP")
            phone["front_camera"] = phone.get("front_camera", "8MP")
            phone["battery"] = phone.get("battery", "5000mAh")

# Save updated data
with open(os.path.join(BASE_DIR, "data", "data.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Added detailed specs to all phones!")
