#!/usr/bin/env python3
"""
Quick bulk phone import script
Just paste data and it adds phones automatically
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

# Popular Indian phones - READY TO IMPORT
PHONES_TO_ADD = [
    # Premium Phones
    {"name": "iPhone 14 Pro", "price": 119999, "gaming": 10, "camera": 10, "battery": 8, "performance": 10, "display": 9, "reason": "Best premium phone with exceptional camera"},
    {"name": "Samsung Galaxy S24", "price": 99999, "gaming": 10, "camera": 9, "battery": 9, "performance": 10, "display": 10, "reason": "Latest Samsung flagship with AI features"},
    {"name": "OnePlus 12", "price": 69999, "gaming": 10, "camera": 8, "battery": 9, "performance": 10, "display": 9, "reason": "Fastest Android phone with smooth performance"},
    
    # High-end Budget Flagship (₹40k-80k)
    {"name": "Realme GT 5 Pro", "price": 79999, "gaming": 10, "camera": 9, "battery": 8, "performance": 10, "display": 10, "reason": "Snapdragon 8 Gen 3 flagship killer"},
    {"name": "Samsung Galaxy S23 FE", "price": 74999, "gaming": 9, "camera": 8, "battery": 8, "performance": 9, "display": 9, "reason": "Samsung flagship experience at lower price"},
    {"name": "Poco F5 Pro", "price": 49999, "gaming": 9, "camera": 8, "battery": 8, "performance": 9, "display": 8, "reason": "Flagship processor at mid-range price"},
    
    # Mid-range Powerhouses (₹20k-40k)
    {"name": "Realme 11 Pro Plus", "price": 36999, "gaming": 8, "camera": 8, "battery": 8, "performance": 8, "display": 9, "reason": "Beautiful phone with pro camera"},
    {"name": "OnePlus Nord CE 3", "price": 29999, "gaming": 8, "camera": 7, "battery": 8, "performance": 8, "display": 8, "reason": "Fast and clean OxygenOS experience"},
    {"name": "Samsung Galaxy A54", "price": 34999, "gaming": 7, "camera": 8, "battery": 9, "performance": 7, "display": 8, "reason": "Samsung's best mid-range offering"},
    {"name": "Poco X5 Pro", "price": 25999, "gaming": 8, "camera": 7, "battery": 8, "performance": 8, "display": 8, "reason": "Great value with fast display"},
    
    # Budget Gaming (₹15k-25k)
    {"name": "Redmi Note 13 Pro Plus", "price": 24999, "gaming": 8, "camera": 8, "battery": 9, "performance": 8, "display": 9, "reason": "Best gaming and camera under ₹25k"},
    {"name": "Realme 11x 5G", "price": 19999, "gaming": 8, "camera": 7, "battery": 8, "performance": 8, "display": 8, "reason": "5G phone at budget price"},
    {"name": "Samsung Galaxy A34", "price": 21999, "gaming": 6, "camera": 7, "battery": 8, "performance": 6, "display": 7, "reason": "Reliable Samsung with good software"},
    {"name": "Poco M6 Pro", "price": 17999, "gaming": 7, "camera": 6, "battery": 8, "performance": 7, "display": 7, "reason": "Good processor for gaming"},
    
    # Entry Level Gaming (₹10k-15k)
    {"name": "Redmi Note 13", "price": 13999, "gaming": 7, "camera": 6, "battery": 8, "performance": 7, "display": 7, "reason": "Best overall value under ₹15k"},
    {"name": "Realme C67", "price": 12999, "gaming": 6, "camera": 6, "battery": 9, "performance": 6, "display": 6, "reason": "Huge battery and clean UI"},
    {"name": "Poco M5", "price": 11999, "gaming": 6, "camera": 5, "battery": 8, "performance": 6, "display": 6, "reason": "Great processor at budget price"},
    {"name": "Samsung Galaxy M14", "price": 12999, "gaming": 5, "camera": 6, "battery": 8, "performance": 5, "display": 6, "reason": "Samsung reliability at budget price"},
    
    # Basic Budget (₹5k-10k)
    {"name": "Redmi A3", "price": 7999, "gaming": 3, "camera": 4, "battery": 7, "performance": 3, "display": 5, "reason": "Best basic phone for calls and WhatsApp"},
    {"name": "Realme C51", "price": 8999, "gaming": 4, "camera": 4, "battery": 7, "performance": 4, "display": 5, "reason": "Good battery for students"},
    {"name": "Infinix Hot 30", "price": 8499, "gaming": 4, "camera": 4, "battery": 8, "performance": 4, "display": 6, "reason": "Largest battery under ₹10k"},
    {"name": "Samsung Galaxy A05", "price": 9999, "gaming": 3, "camera": 5, "battery": 7, "performance": 3, "display": 5, "reason": "Samsung's entry level option"},
]

def main():
    print("="*60)
    print("BULK PHONE IMPORT")
    print("="*60)
    
    # Load existing data
    data = load_data()
    initial_count = len(data["mobiles"])
    
    print(f"\n📱 Current phones in database: {initial_count}")
    print(f"➕ About to add: {len(PHONES_TO_ADD)} new phones\n")
    
    # Add phones
    added = 0
    skipped = 0
    
    for phone in PHONES_TO_ADD:
        # Check if phone already exists
        exists = False
        for existing in data["mobiles"]:
            if existing["name"].lower() == phone["name"].lower():
                exists = True
                break
        
        if exists:
            print(f"⏭️  Skipped: {phone['name']} (already exists)")
            skipped += 1
        else:
            # Add amazon and flipkart links
            phone["image"] = "https://m.media-amazon.com/images/I/81t6Av5DvXL._SL1500_.jpg"
            phone["amazon"] = f"https://www.amazon.in/s?k={phone['name'].replace(' ', '+')}"
            phone["flipkart"] = f"https://www.flipkart.com/search?q={phone['name']}"
            
            data["mobiles"].append(phone)
            added += 1
            print(f"✓ Added: {phone['name']} - ₹{phone['price']}")
    
    # Save data
    save_data(data)
    
    print("\n" + "="*60)
    print(f"✓ Added: {added} phones")
    print(f"⏭️  Skipped: {skipped} phones (already in database)")
    print(f"📊 Total phones now: {len(data['mobiles'])}")
    print("="*60)

if __name__ == "__main__":
    main()
