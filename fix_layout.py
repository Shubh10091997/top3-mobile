#!/usr/bin/env python3
import re

# Read current index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove duplicate header
old_header = '''  <!-- Header with Wishlist Button -->
  <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
    <h1 style="margin: 0; color: white; font-size: 22px;">🏆 Top3Pick</h1>
    <button onclick="viewWishlist()" class="wishlist-header-btn" style="background: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600; color: #667eea; transition: all 0.3s;">
      ❤️ Wishlist (<span id="wishlistCount" style="font-weight: 700;">0</span>)
    </button>
  </div>


<div class="container-wrapper">'''

new_header = '''
<div class="container-wrapper">'''

content = content.replace(old_header, new_header)

# 2. Fix feature cards grid - make responsive and prevent overflow
old_features = '''  <!-- Enhanced Features Section - Top 3 Style -->
  <div class="features-section" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; padding: 0 20px;">'''

new_features = '''  <!-- Enhanced Features Section - Top 3 Style -->
  <div class="features-section" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 30px 0; padding: 0; width: 100%; box-sizing: border-box;">'''

content = content.replace(old_features, new_features)

# 3. Fix feature card padding/sizing for smaller screens
old_card_style = '''    <div class="feature-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);">'''

new_card_style = '''    <div class="feature-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 12px; padding: 20px 15px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">'''

content = re.sub(r'<div class="feature-card" style="background: linear-gradient\(135deg, #f093fb, #f5576c\);[^"]*">', new_card_style, content)

# Similar fix for other feature cards
content = re.sub(r'<div class="feature-card" style="background: linear-gradient\(135deg, #4facfe, #00f2fe\);[^"]*">', 
    '''<div class="feature-card" style="background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 12px; padding: 20px 15px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">''', content)

content = re.sub(r'<div class="feature-card" style="background: linear-gradient\(135deg, #fa709a, #fee140\);[^"]*">', 
    '''<div class="feature-card" style="background: linear-gradient(135deg, #fa709a, #fee140); border-radius: 12px; padding: 20px 15px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(250, 112, 154, 0.3); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">''', content)

# Fix the first one that doesn't have pattern
content = content.replace(
    '''<div class="feature-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);">''',
    '''<div class="feature-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 12px; padding: 20px 15px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">'''
)

# 4. Add responsive CSS for mobile
responsive_css = '''

  /* Responsive Feature Cards */
  @media (max-width: 1200px) {
    .features-section {
      grid-template-columns: repeat(3, 1fr) !important;
      gap: 12px !important;
    }
  }

  @media (max-width: 768px) {
    .features-section {
      grid-template-columns: 1fr !important;
      gap: 12px !important;
    }
  }
'''

# Find the last @media block and add before it
media_pos = content.rfind('@media (max-width: 768px) {')
if media_pos > 0:
    content = content[:media_pos] + responsive_css + content[media_pos:]

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed layout issues!")
print("✅ Removed duplicate headers")
print("✅ Fixed feature cards overflow")
print("✅ Made responsive for all screens")
