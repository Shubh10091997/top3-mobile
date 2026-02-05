import re

# Read the HTML file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the phone card template and replace with specs
old_pattern = r'(<div class="kb-phone-price">₹\$\{phone\.price\.toLocaleString\(\)\}<\/div>)\s*(<div class="kb-phone-score">🎮 Gaming)'

new_replacement = r'''\1
          <div style="font-size: 11px; color: #999; margin: 6px 0;">
            📱 ${phone.ram || '4GB'} RAM | 💾 ${phone.storage || '64GB'} <br>
            🎯 ${phone.processor || 'Unknown'} <br>
            📷 ${phone.main_camera || '50MP'} | 🔋 ${phone.battery || '5000mAh'}
          </div>
          \2'''

# Replace all occurrences
content = re.sub(old_pattern, new_replacement, content)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated all phone cards with detailed specs!")
