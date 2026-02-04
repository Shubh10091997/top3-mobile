#!/usr/bin/env python3
"""
CSV Phone Importer
Imports phones from CSV file and adds them to the database
"""

import json
import os
import csv
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "data.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_csv(csv_path):
    """Parse CSV and convert to phone data format"""
    phones = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map CSV columns to phone data structure
            phone = {
                "name": row.get("name", "").strip(),
                "price": int(row.get("price", 0)) if row.get("price") else 0,
                "image": row.get("img", "").strip() or "/static/no-image.png",
                "amazon": f"https://www.amazon.in/s?k={row.get('name', '').replace(' ', '+')}" if row.get("name") else "",
                "flipkart": f"https://www.flipkart.com/search?q={row.get('name')}" if row.get("name") else "",
                
                # Specs - use rating as base for scoring (0-5 scale converted to 0-10)
                "gaming": min(10, int(float(row.get("rating", 5)) * 2)) if row.get("rating") else 5,
                "camera": min(10, int(float(row.get("rating", 5)) * 2)) if row.get("rating") else 5,
                "battery": min(10, int(float(row.get("rating", 5)) * 2)) if row.get("rating") else 5,
                "performance": min(10, int(float(row.get("rating", 5)) * 2)) if row.get("rating") else 5,
                "display": min(10, int(float(row.get("rating", 5)) * 2)) if row.get("rating") else 5,
                
                # Info
                "reason": f"{row.get('company', '')} {row.get('processor', '')}".strip() or "Quality phone",
                "company": row.get("company", "").strip(),
                "processor": row.get("processor", "").strip(),
                
                # Features
                "ram": row.get("ram", "").strip(),
                "storage": row.get("ram (inbuilt)", "").strip(),
                "battery_mah": row.get("battery (in mAh)", "").strip(),
                "display_size": row.get("display size", "").strip(),
                "4g": row.get("4G", "").strip().lower() == "true",
                "5g": row.get("5G", "").strip().lower() == "true",
                "nfc": row.get("NFC", "").strip().lower() == "true",
                "front_camera": row.get("front_camera", "").strip(),
                "rear_camera": row.get("rear_camera", "").strip(),
            }
            
            # Only add if name and price exist
            if phone["name"] and phone["price"] > 0:
                phones.append(phone)
    
    return phones

def main():
    # CSV file path
    csv_path = r"c:\Users\Shubham\Downloads\PHONES\phones.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    print("="*70)
    print("CSV PHONE IMPORTER")
    print("="*70)
    
    # Parse CSV
    print(f"\n📂 Reading CSV file: {csv_path}")
    phones = parse_csv(csv_path)
    print(f"✓ Parsed {len(phones)} phones from CSV\n")
    
    # Load existing data
    data = load_data()
    initial_count = len(data["mobiles"])
    print(f"📱 Current phones in database: {initial_count}")
    
    # Add phones (avoid duplicates)
    added = 0
    skipped = 0
    
    for phone in phones:
        # Check if phone already exists (case-insensitive)
        exists = False
        for existing in data["mobiles"]:
            if existing["name"].lower() == phone["name"].lower():
                exists = True
                break
        
        if exists:
            skipped += 1
            print(f"⏭️  Skipped: {phone['name']} (already exists)")
        else:
            data["mobiles"].append(phone)
            added += 1
            print(f"✓ Added: {phone['name']} - ₹{phone['price']}")
    
    # Save data
    save_data(data)
    
    print("\n" + "="*70)
    print(f"✅ Import Complete!")
    print(f"   Added: {added} phones")
    print(f"   Skipped: {skipped} phones (duplicates)")
    print(f"   Total in database: {len(data['mobiles'])} phones")
    print("="*70)

if __name__ == "__main__":
    main()
