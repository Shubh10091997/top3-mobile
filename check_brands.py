#!/usr/bin/env python3
import json

with open('data/data.json') as f:
    data = json.load(f)

# Get unique brands
brands = {}
for phone in data['mobiles']:
    brand = phone.get('company', phone.get('name', 'Unknown').split()[0])
    if brand not in brands:
        brands[brand] = []
    brands[brand].append(phone)

# Sort by count
sorted_brands = sorted(brands.items(), key=lambda x: len(x[1]), reverse=True)

print("="*60)
print("BRAND DISTRIBUTION")
print("="*60)
print(f"\nTotal Unique Brands: {len(brands)}\n")

for brand, phones in sorted_brands[:20]:  # Top 20
    prices = [p['price'] for p in phones]
    print(f"  {brand:20} | {len(phones):4} phones | ₹{min(prices):,} - ₹{max(prices):,}")

print(f"\n... and {len(sorted_brands)-20} more brands" if len(sorted_brands) > 20 else "")
print("="*60)
