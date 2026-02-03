#!/usr/bin/env python3
"""
Script to add phones to database easily
Run: python add_phones.py
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "data.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_phone():
    """Add a single phone interactively"""
    print("\n" + "="*50)
    print("ADD NEW PHONE")
    print("="*50)
    
    phone = {}
    
    phone["name"] = input("Phone name (e.g., Realme C55): ").strip()
    phone["price"] = int(input("Price in ₹ (e.g., 10000): ").strip())
    phone["image"] = input("Image URL (paste Amazon/Flipkart image link): ").strip()
    phone["reason"] = input("Why this phone? (e.g., Best gaming performance): ").strip()
    
    print("\nRate this phone (0-10 scale):")
    phone["gaming"] = int(input("  Gaming score (0-10): "))
    phone["camera"] = int(input("  Camera score (0-10): "))
    phone["battery"] = int(input("  Battery score (0-10): "))
    phone["performance"] = int(input("  Performance score (0-10): "))
    phone["display"] = int(input("  Display score (0-10): "))
    
    phone["amazon"] = input("Amazon search link (or press Enter to skip): ").strip() or f"https://www.amazon.in/s?k={phone['name'].replace(' ', '+')}"
    phone["flipkart"] = input("Flipkart search link (or press Enter to skip): ").strip() or f"https://www.flipkart.com/search?q={phone['name']}"
    
    return phone

def bulk_add_phones():
    """Add multiple phones from a list"""
    print("\n" + "="*50)
    print("BULK ADD PHONES (copy-paste format)")
    print("="*50)
    print("""
Format (comma-separated):
name,price,gaming,camera,battery,performance,display,reason

Example:
Realme C55,10000,7,6,7,6,6,Best gaming performance under ₹10k
iPhone 12,65000,9,9,8,9,9,Premium Apple phone

Paste your data below (one phone per line). Press Enter twice when done:
    """)
    
    phones = []
    while True:
        line = input().strip()
        if not line:
            break
        
        try:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 8:
                phone = {
                    "name": parts[0],
                    "price": int(parts[1]),
                    "gaming": int(parts[2]),
                    "camera": int(parts[3]),
                    "battery": int(parts[4]),
                    "performance": int(parts[5]),
                    "display": int(parts[6]),
                    "reason": parts[7],
                    "image": "https://m.media-amazon.com/images/I/81t6Av5DvXL._SL1500_.jpg",
                    "amazon": f"https://www.amazon.in/s?k={parts[0].replace(' ', '+')}",
                    "flipkart": f"https://www.flipkart.com/search?q={parts[0]}"
                }
                phones.append(phone)
                print(f"✓ Added: {phone['name']}")
        except (ValueError, IndexError):
            print(f"✗ Skipped invalid line: {line}")
    
    return phones

def view_phones():
    """View all phones in database"""
    data = load_data()
    print("\n" + "="*50)
    print(f"TOTAL MOBILES: {len(data['mobiles'])}")
    print("="*50)
    
    for i, phone in enumerate(data['mobiles'], 1):
        print(f"\n{i}. {phone['name']}")
        print(f"   Price: ₹{phone['price']}")
        print(f"   Gaming: {phone['gaming']}/10 | Camera: {phone['camera']}/10 | Battery: {phone['battery']}/10")

def main():
    while True:
        print("\n" + "="*50)
        print("PHONE DATABASE MANAGER")
        print("="*50)
        print("1. Add single phone")
        print("2. Add multiple phones (bulk)")
        print("3. View all phones")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            phone = add_phone()
            data = load_data()
            data["mobiles"].append(phone)
            save_data(data)
            print(f"\n✓ Added '{phone['name']}' to database!")
        
        elif choice == "2":
            phones = bulk_add_phones()
            if phones:
                data = load_data()
                data["mobiles"].extend(phones)
                save_data(data)
                print(f"\n✓ Added {len(phones)} phones to database!")
        
        elif choice == "3":
            view_phones()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
