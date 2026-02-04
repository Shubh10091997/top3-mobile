#!/usr/bin/env python3
"""Quick verification script"""
import json

with open('data/data.json') as f:
    data = json.load(f)

print("="*60)
print("DATABASE VERIFICATION")
print("="*60)
print(f"\n📱 Total Phones: {len(data['mobiles'])}")
print(f"🏍️  Total Bikes: {len(data.get('bikes', []))}")
print(f"\n✓ First 10 imported phones:")
for phone in data['mobiles'][:10]:
    print(f"  • {phone['name']} - ₹{phone['price']}")
print("\n" + "="*60)
