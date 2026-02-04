#!/usr/bin/env python3
import re

# Read the current index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add wishlist header button after <body> tag
header_html = '''
  <!-- Header with Wishlist Button -->
  <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
    <h1 style="margin: 0; color: white; font-size: 22px;">🏆 Top3Pick</h1>
    <button onclick="viewWishlist()" class="wishlist-header-btn" style="background: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600; color: #667eea; transition: all 0.3s;">
      ❤️ Wishlist (<span id="wishlistCount" style="font-weight: 700;">0</span>)
    </button>
  </div>
'''

# Insert after <body>
content = content.replace('<body>', '<body>' + header_html)

# 2. Update phone cards to include wishlist button
# Find the kb-phone-card pattern and add wishlist button
old_card_pattern = r'<div class="kb-phone-card">\s+<input type="checkbox"'
new_card_html = '''<div class="kb-phone-card">
          <button class="wishlist-btn" data-phone="${phone.name}" onclick="toggleWishlist('${phone.name}'); updateWishlistUI(); event.stopPropagation();" style="position: absolute; top: 8px; right: 8px; background: none; border: none; font-size: 20px; cursor: pointer; z-index: 10;">❤️</button>
          <input type="checkbox"'''

content = re.sub(old_card_pattern, new_card_html, content)

# 3. Add wishlist CSS styles before </style>
wishlist_css = '''

  /* ===== WISHLIST STYLES ===== */
  .wishlist-header-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .wishlist-btn {
    transition: all 0.3s;
    opacity: 0.6;
  }

  .wishlist-btn:hover {
    opacity: 1;
    transform: scale(1.2);
  }

  .wishlist-btn.in-wishlist {
    opacity: 1;
    animation: heartbeat 0.3s;
  }

  @keyframes heartbeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
  }

  .wishlist-modal {
    background: white;
    border-radius: 15px;
    padding: 30px;
    max-width: 600px;
    width: 100%;
  }

  .wishlist-modal h3 {
    margin: 0 0 20px 0;
    font-size: 24px;
    color: #667eea;
  }

  .wishlist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 15px;
  }

  .wishlist-card {
    background: #f5f7ff;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    position: relative;
    border: 2px solid #e8ebf8;
  }

  .wishlist-card h4 {
    margin: 10px 0 8px 0;
    font-size: 14px;
    color: #1f2a44;
  }

  .wishlist-card .price {
    color: #667eea;
    font-weight: 700;
    font-size: 16px;
    margin: 5px 0;
  }

  .wishlist-card .brand {
    color: #999;
    font-size: 12px;
    margin: 8px 0;
  }

  .remove-wishlist {
    position: absolute;
    top: 5px;
    right: 5px;
    background: #ff6b6b;
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
  }

  .remove-wishlist:hover {
    background: #ff4757;
    transform: rotate(90deg);
  }

  .compare-link {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 12px;
    margin-top: 8px;
    transition: all 0.3s;
  }

  .compare-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .kb-phone-card {
    position: relative;
  }
'''

# Insert CSS before closing </style> tag
content = content.replace('  @media (max-width: 768px) {', wishlist_css + '\n  @media (max-width: 768px) {')

# 4. Add wishlist JavaScript code before closing </script> tag
wishlist_js = '''

  // ===== WISHLIST FEATURE =====
  let wishlist = JSON.parse(localStorage.getItem('phoneWishlist')) || [];

  function toggleWishlist(phoneName) {
    const index = wishlist.indexOf(phoneName);
    if (index > -1) {
      wishlist.splice(index, 1);
    } else {
      wishlist.push(phoneName);
    }
    localStorage.setItem('phoneWishlist', JSON.stringify(wishlist));
    updateWishlistUI();
  }

  function updateWishlistUI() {
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
  }

  function viewWishlist() {
    if (wishlist.length === 0) {
      alert('Your wishlist is empty! ❤️');
      return;
    }
    
    let html = '<div class="wishlist-modal">';
    html += '<h3>❤️ My Wishlist (' + wishlist.length + ')</h3>';
    html += '<div class="wishlist-grid">';
    
    wishlist.forEach(name => {
      const phone = allPhones.find(p => p.name === name);
      if (phone) {
        html += `
          <div class="wishlist-card">
            <button class="remove-wishlist" onclick="toggleWishlist('${phone.name}'); updateWishlistUI(); this.closest('[style*=\\\"position:fixed\\\"]').remove();">✕</button>
            <h4>${phone.name}</h4>
            <p class="price">₹${phone.price.toLocaleString()}</p>
            <p class="brand">${phone.company || 'Brand'}</p>
            <a href="javascript:void(0)" class="compare-link" onclick="document.getElementById('kbSearch').value='${phone.name}'; performKBSearch(); this.closest('[style*=\\\"position:fixed\\\"]').remove();">Compare</a>
          </div>
        `;
      }
    });
    
    html += '</div></div>';
    
    const modal = document.createElement('div');
    modal.innerHTML = html;
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:2000;display:flex;align-items:center;justify-content:center;';
    modal.onclick = function(e) {
      if (e.target === modal) modal.remove();
    };
    document.body.appendChild(modal);
  }

  // Initialize on page load
  setTimeout(() => updateWishlistUI(), 500);
'''

# Insert before closing </script>
content = content.replace('  loadPhones();', wishlist_js + '\n\n  loadPhones();')

# Write the updated content back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Wishlist feature added successfully!")
print("❤️ Users can now save phones to wishlist")
print("📍 Wishlist saves in browser storage (localStorage)")
