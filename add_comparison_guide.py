#!/usr/bin/env python3
import re

# Read current index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add step-by-step comparison guide modal
guide_html = '''
  <!-- Comparison Guide Modal -->
  <div id="comparisonGuideModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 3500; align-items: center; justify-content: center;">
    <div style="background: white; border-radius: 20px; padding: 30px; max-width: 600px; width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 24px; color: #667eea;">⚖️ How to Compare Phones</h3>
        <button onclick="document.getElementById('comparisonGuideModal').style.display='none';" style="background: none; border: none; font-size: 24px; cursor: pointer;">✕</button>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <!-- Step 1 -->
        <div style="background: #f5f7ff; padding: 20px; border-radius: 12px; border-left: 4px solid #667eea;">
          <div style="font-size: 36px; margin-bottom: 10px;">1️⃣</div>
          <h4 style="margin: 0 0 8px 0; color: #667eea; font-weight: 700;">Search</h4>
          <p style="margin: 0; font-size: 13px; color: #5b667a;">Type phone name or filter by specs in the Knowledge Base section</p>
        </div>

        <!-- Step 2 -->
        <div style="background: #fff5f7; padding: 20px; border-radius: 12px; border-left: 4px solid #f5576c;">
          <div style="font-size: 36px; margin-bottom: 10px;">2️⃣</div>
          <h4 style="margin: 0 0 8px 0; color: #f5576c; font-weight: 700;">Select</h4>
          <p style="margin: 0; font-size: 13px; color: #5b667a;">Click checkbox ☑️ on phone cards to select (max 3 phones)</p>
        </div>

        <!-- Step 3 -->
        <div style="background: #f0f9ff; padding: 20px; border-radius: 12px; border-left: 4px solid #4facfe;">
          <div style="font-size: 36px; margin-bottom: 10px;">3️⃣</div>
          <h4 style="margin: 0 0 8px 0; color: #4facfe; font-weight: 700;">View Counter</h4>
          <p style="margin: 0; font-size: 13px; color: #5b667a;">See "Selected: X/3" in right sidebar counter</p>
        </div>

        <!-- Step 4 -->
        <div style="background: #fffbf0; padding: 20px; border-radius: 12px; border-left: 4px solid #fa709a;">
          <div style="font-size: 36px; margin-bottom: 10px;">4️⃣</div>
          <h4 style="margin: 0 0 8px 0; color: #fa709a; font-weight: 700;">Compare</h4>
          <p style="margin: 0; font-size: 13px; color: #5b667a;">Click "Compare Selected Phones" button to open comparison</p>
        </div>
      </div>

      <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 15px; margin-top: 20px;">
        <strong style="color: #856404;">💡 Tip:</strong> Select at least 2 phones to enable compare button. You can compare up to 3 phones at once.
      </div>

      <button onclick="document.getElementById('comparisonGuideModal').style.display='none';" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; margin-top: 20px; font-size: 16px;">Got It! Let's Compare</button>
    </div>
  </div>
'''

content = content.replace('</body>', guide_html + '\n</body>')

# Update the Compare Card to show the guide
old_compare_card = '''<button onclick="document.getElementById('compareBtn').style.display='block'; document.querySelector('.compare-bar').style.display='flex';" style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.3s;">Start Compare</button>'''

new_compare_card = '''<button onclick="document.getElementById('comparisonGuideModal').style.display='flex';" style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.3s;">Learn & Compare</button>'''

content = content.replace(old_compare_card, new_compare_card)

# Add visual step indicators in the comparison sidebar
# Find the compare bar and enhance it
old_compare_bar = '''<div style="margin-bottom: 20px;">
        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #1f2a44;">💰 Price Range</label>'''

new_compare_section = '''<div style="background: #f5f7ff; border-radius: 12px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #667eea;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h4 style="margin: 0; color: #667eea; font-size: 16px; font-weight: 700;">📊 Comparison Status</h4>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: #5b667a;">Select 2-3 phones to compare</p>
          </div>
          <div style="font-size: 24px;">⚖️</div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 12px;">
          <div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #ddd;">
            <div style="font-size: 20px; color: #667eea; font-weight: 700;" id="selectedCount1">0</div>
            <div style="font-size: 10px; color: #999;">Selected</div>
          </div>
          <div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #ddd;">
            <div style="font-size: 20px; color: #4facfe; font-weight: 700;">3</div>
            <div style="font-size: 10px; color: #999;">Max</div>
          </div>
          <div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border: 2px solid #ddd;">
            <div style="font-size: 20px; color: #f5576c; font-weight: 700;" id="remainCount">3</div>
            <div style="font-size: 10px; color: #999;">Remaining</div>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #1f2a44;">💰 Price Range</label>'''

content = content.replace(old_compare_bar, new_compare_section)

# Update the JavaScript to update the comparison status counter
status_update_js = '''
  function updateWishlistUI() {
    const count = document.getElementById('wishlistCount');
    if (count) {
      count.textContent = wishlist.length;
    }
    
    // Update comparison status
    const selectedCount = document.getElementById('selectedCount1');
    const remainCount = document.getElementById('remainCount');
    if (selectedCount) {
      selectedCount.textContent = selectedPhones.length;
    }
    if (remainCount) {
      remainCount.textContent = 3 - selectedPhones.length;
    }
    
    // Update all heart icons
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
      const phoneName = btn.dataset.phone;
      if (wishlist.includes(phoneName)) {
        btn.classList.add('in-wishlist');
      } else {
        btn.classList.remove('in-wishlist');
      }
    });
  }
'''

old_update_fn = '''  function updateWishlistUI() {
    const count = document.getElementById('wishlistCount');
    if (count) {
      count.textContent = wishlist.length;
    }
    
    // Update all heart icons
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
      const phoneName = btn.dataset.phone;
      if (wishlist.includes(phoneName)) {
        btn.classList.add('in-wishlist');
      } else {
        btn.classList.remove('in-wishlist');
      }
    });
  }'''

content = content.replace(old_update_fn, status_update_js)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Comparison guide added!")
print("⚖️ Step-by-step instructions modal")
print("📊 Real-time selection counter")
print("💡 User-friendly tooltips")
