#!/usr/bin/env python3
import re

# Read the current index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the header style to match top 3 design
new_header = '''
  <!-- Header with Wishlist Button - Top 3 Style -->
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white;">
    <h1 style="margin: 0; font-size: 28px; font-weight: 700;">🏆 Top 3 Best Options</h1>
    <p style="margin: 8px 0 0 0; font-size: 14px; opacity: 0.9;">Compare Phones with Our Smart Features</p>
    <button onclick="viewWishlist()" class="wishlist-header-btn" style="background: rgba(255,255,255,0.2); border: 2px solid white; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: 600; margin-top: 12px; transition: all 0.3s; font-size: 14px;">
      ❤️ My Wishlist <span id="wishlistCount" style="background: #ff6b6b; border-radius: 50%; padding: 0 6px;">0</span>
    </button>
  </div>
'''

content = content.replace('<body>', '<body>' + new_header)

# 2. Add new feature cards section (Wishlist, Filters, Export) styled like top 3
feature_section = '''
  <!-- Enhanced Features Section - Top 3 Style -->
  <div class="features-section" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; padding: 0 20px;">
    <!-- Wishlist Card -->
    <div class="feature-card" style="background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);">
      <div style="font-size: 40px; margin-bottom: 12px;">❤️</div>
      <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">My Wishlist</h3>
      <p style="margin: 0 0 16px 0; font-size: 13px; opacity: 0.95;">Save phones for later</p>
      <button onclick="viewWishlist()" style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.3s;">View Saved</button>
    </div>

    <!-- Filter Card -->
    <div class="feature-card" style="background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);">
      <div style="font-size: 40px; margin-bottom: 12px;">🔍</div>
      <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">Smart Filters</h3>
      <p style="margin: 0 0 16px 0; font-size: 13px; opacity: 0.95;">Filter by specs & price</p>
      <button onclick="showAdvancedFilters()" style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.3s;">Open Filters</button>
    </div>

    <!-- Compare Card -->
    <div class="feature-card" style="background: linear-gradient(135deg, #fa709a, #fee140); border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);">
      <div style="font-size: 40px; margin-bottom: 12px;">⚖️</div>
      <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">Compare Phones</h3>
      <p style="margin: 0 0 16px 0; font-size: 13px; opacity: 0.95;">Select & compare specs</p>
      <button onclick="document.getElementById('compareBtn').style.display='block'; document.querySelector('.compare-bar').style.display='flex';" style="background: rgba(255,255,255,0.3); border: 2px solid white; color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.3s;">Start Compare</button>
    </div>
  </div>
'''

# Insert after the knowledge cards section
knowledge_cards_close = content.find('      </div>\n\n      <!-- Quick Filter Cards -->')
if knowledge_cards_close > 0:
    content = content[:knowledge_cards_close] + '      </div>' + feature_section + '\n      <!-- Quick Filter Cards -->' + content[knowledge_cards_close + len('      </div>\n\n      <!-- Quick Filter Cards -->'):]

# 3. Add Advanced Filters Modal HTML (Top 3 Style)
advanced_filters_html = '''
  <!-- Advanced Filters Modal -->
  <div id="advancedFiltersModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 3000; align-items: center; justify-content: center;">
    <div style="background: white; border-radius: 20px; padding: 30px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 22px; color: #667eea;">🔍 Smart Filters</h3>
        <button onclick="document.getElementById('advancedFiltersModal').style.display='none';" style="background: none; border: none; font-size: 24px; cursor: pointer;">✕</button>
      </div>

      <div style="margin-bottom: 20px;">
        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #1f2a44;">💰 Price Range</label>
        <div style="display: flex; gap: 10px;">
          <input type="range" id="priceMin" min="5000" max="100000" value="5000" style="flex: 1; cursor: pointer;">
          <span id="priceMinVal">₹5000</span>
        </div>
        <div style="display: flex; gap: 10px; margin-top: 10px;">
          <input type="range" id="priceMax" min="5000" max="200000" value="100000" style="flex: 1; cursor: pointer;">
          <span id="priceMaxVal">₹100000</span>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #1f2a44;">🎮 Best For</label>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <button onclick="filterBySpecAdvanced('gaming')" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600;">Gaming</button>
          <button onclick="filterBySpecAdvanced('camera')" style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600;">Camera</button>
          <button onclick="filterBySpecAdvanced('battery')" style="background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600;">Battery</button>
          <button onclick="filterBySpecAdvanced('performance')" style="background: linear-gradient(135deg, #fa709a, #fee140); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600;">Performance</button>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #1f2a44;">📱 Brands</label>
        <div id="brandCheckboxes" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-height: 150px; overflow-y: auto;">
          <!-- Populated by JavaScript -->
        </div>
      </div>

      <button onclick="applyAdvancedFilters(); document.getElementById('advancedFiltersModal').style.display='none';" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; font-size: 16px;">Apply Filters</button>
    </div>
  </div>
'''

# Insert before </body>
content = content.replace('</body>', advanced_filters_html + '\n</body>')

# 4. Add JavaScript functions for filters
filters_js = '''

  // ===== ADVANCED FILTERS =====
  function showAdvancedFilters() {
    document.getElementById('advancedFiltersModal').style.display = 'flex';
    populateBrandCheckboxes();
  }

  function populateBrandCheckboxes() {
    const brands = [...new Set(allPhones.map(p => p.company))].filter(b => b);
    const container = document.getElementById('brandCheckboxes');
    container.innerHTML = '';
    brands.forEach(brand => {
      const label = document.createElement('label');
      label.style.cssText = 'display: flex; align-items: center; gap: 8px; cursor: pointer;';
      label.innerHTML = `
        <input type="checkbox" value="${brand}" style="cursor: pointer;">
        <span>${brand}</span>
      `;
      container.appendChild(label);
    });
  }

  function filterBySpecAdvanced(spec) {
    document.getElementById('kbSpecFilter').value = spec;
    performKBSearch();
  }

  function applyAdvancedFilters() {
    const priceMin = parseInt(document.getElementById('priceMin').value);
    const priceMax = parseInt(document.getElementById('priceMax').value);
    const selectedBrands = Array.from(document.querySelectorAll('#brandCheckboxes input:checked')).map(cb => cb.value);
    
    let filtered = allPhones.filter(phone => 
      phone.price >= priceMin && 
      phone.price <= priceMax && 
      (selectedBrands.length === 0 || selectedBrands.includes(phone.company))
    );

    const grid = document.getElementById('kbPhonesGrid');
    const resultsDiv = document.getElementById('kbResults');
    
    if (filtered.length === 0) {
      grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: rgba(255,255,255,0.7);">No phones match your filters</p>';
      resultsDiv.style.display = 'block';
      return;
    }

    let html = '';
    filtered.slice(0, 8).forEach(phone => {
      html += `
        <div class="kb-phone-card">
          <button class="wishlist-btn" data-phone="${phone.name}" onclick="toggleWishlist('${phone.name}'); updateWishlistUI(); event.stopPropagation();" style="position: absolute; top: 8px; right: 8px; background: none; border: none; font-size: 20px; cursor: pointer; z-index: 10;">❤️</button>
          <input type="checkbox" class="phone-checkbox" onchange="togglePhoneSelection('${phone.name}')" />
          <div class="kb-phone-name">${phone.name}</div>
          <div class="kb-phone-price">₹${phone.price.toLocaleString()}</div>
          <div class="kb-phone-score">🎮 Gaming: ${phone.gaming || 5}/10</div>
          <div class="kb-phone-score">📷 Camera: ${phone.camera || 5}/10</div>
          <div class="kb-phone-score">🔋 Battery: ${phone.battery || 5}/10</div>
          <div class="kb-phone-score">⚡ Performance: ${phone.performance || 5}/10</div>
        </div>
      `;
    });
    
    grid.innerHTML = html;
    resultsDiv.style.display = 'block';
    updateWishlistUI();
  }

  // Update price range display
  document.addEventListener('DOMContentLoaded', function() {
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    if (priceMin) {
      priceMin.addEventListener('input', function() {
        document.getElementById('priceMinVal').textContent = '₹' + parseInt(this.value).toLocaleString();
      });
    }
    if (priceMax) {
      priceMax.addEventListener('input', function() {
        document.getElementById('priceMaxVal').textContent = '₹' + parseInt(this.value).toLocaleString();
      });
    }
  });
'''

# Insert before closing </script>
content = content.replace('  // Initialize on page load\n  setTimeout(() => updateWishlistUI(), 500);', filters_js + '\n\n  // Initialize on page load\n  setTimeout(() => updateWishlistUI(), 500);')

# Write the updated content back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All features added with Top 3 Card Design!")
print("❤️ Wishlist with heart icons")
print("🔍 Advanced Smart Filters")
print("⚖️ Phone Comparison with checkboxes")
print("🎨 Gradient cards matching your original design")
