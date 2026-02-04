#!/usr/bin/env python3
import re

# Read the current index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add comparison modal HTML before the closing tag of knowledge-section
comparison_modal_html = '''

      <!-- Comparison Modal -->
      <div id="comparisonModal" class="comparison-modal" style="display:none;">
        <div class="comparison-modal-content">
          <button onclick="closeComparison()" class="close-btn">✕</button>
          <h3>📊 Phone Comparison</h3>
          <div class="comparison-table" id="comparisonTable"></div>
        </div>
      </div>'''

# Find the position to insert (before the closing </div> of knowledge-section)
knowledge_section_close = content.find('    </div>\n\n    <!-- Right Side: Popular Specifications -->')
if knowledge_section_close > 0:
    content = content[:knowledge_section_close] + comparison_modal_html + '\n' + content[knowledge_section_close:]

# 2. Add compare bar HTML before the closing </div> of kb-results
compare_bar_html = '''
        <div class="compare-bar" id="compareBar" style="display:none;">
          <span id="compareCount">Selected: 0/3</span>
          <button id="compareBtn" onclick="openComparison()" style="display:none;" class="compare-button">
            ⚖️ Compare Selected Phones
          </button>
        </div>'''

kb_results_close = content.find('        </div>\n      </div>\n    </div>\n\n    <!-- Right Side: Popular Specifications -->')
if kb_results_close > 0:
    content = content[:kb_results_close] + '\n' + compare_bar_html + '\n' + content[kb_results_close:]

# 3. Add comparison functions to JavaScript
comparison_functions = '''
  // Phone database from server
  let allPhones = [];
  let selectedPhones = [];

  function togglePhoneSelection(phoneName) {
    const index = selectedPhones.indexOf(phoneName);
    if (index > -1) {
      selectedPhones.splice(index, 1);
    } else if (selectedPhones.length < 3) {
      selectedPhones.push(phoneName);
    }
    updateCompareButton();
  }

  function updateCompareButton() {
    const count = document.getElementById('compareCount');
    if (count) {
      count.textContent = `Selected: ${selectedPhones.length}/3`;
    }
    const btn = document.getElementById('compareBtn');
    const bar = document.getElementById('compareBar');
    if (btn && bar) {
      if (selectedPhones.length >= 2) {
        btn.style.display = 'inline-block';
        bar.style.display = 'flex';
      } else {
        btn.style.display = 'none';
        if (selectedPhones.length === 0) {
          bar.style.display = 'none';
        }
      }
    }
  }

  function openComparison() {
    const modal = document.getElementById('comparisonModal');
    const table = document.getElementById('comparisonTable');
    
    if (!modal || !table || selectedPhones.length < 2) return;
    
    let html = '<div class="comparison-specs">';
    const specs = ['price', 'ram', 'processor', 'storage', 'camera', 'battery', 'display', 'gaming', 'camera_score', 'battery_score', 'performance'];
    
    html += '<div class="spec-row"><div class="spec-name">Specs</div>';
    selectedPhones.forEach(name => {
      html += `<div class="spec-value phone-header">${name}</div>`;
    });
    html += '</div>';
    
    specs.forEach(spec => {
      html += '<div class="spec-row"><div class="spec-name">' + spec.toUpperCase().replace(/_/g, ' ') + '</div>';
      selectedPhones.forEach(name => {
        const phone = allPhones.find(p => p.name === name);
        const value = phone && phone[spec] ? phone[spec] : 'N/A';
        html += `<div class="spec-value">${value}</div>`;
      });
      html += '</div>';
    });
    
    html += '</div>';
    table.innerHTML = html;
    modal.style.display = 'flex';
  }

  function closeComparison() {
    const modal = document.getElementById('comparisonModal');
    if (modal) {
      modal.style.display = 'none';
    }
  }
'''

# Replace the old allPhones declaration
content = content.replace('  // Phone database from server\n  let allPhones = [];', comparison_functions)

# 4. Add checkboxes to phone cards in the performKBSearch function
old_card_pattern = r'<div class="kb-phone-card">\s+<div class="kb-phone-name">'
new_card_html = '<div class="kb-phone-card">\n          <input type="checkbox" class="phone-checkbox" onchange="togglePhoneSelection(\'${phone.name}\')" />\n          <div class="kb-phone-name">'

content = re.sub(old_card_pattern, new_card_html, content)

# 5. Add CSS styles
css_styles = '''

  /* ===== COMPARISON FEATURE STYLES ===== */
  .compare-bar {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  }

  .compare-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.3s;
  }

  .compare-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  }

  .comparison-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    z-index: 1000;
    align-items: center;
    justify-content: center;
  }

  .comparison-modal-content {
    background: white;
    border-radius: 15px;
    padding: 25px;
    max-width: 95%;
    max-height: 85%;
    overflow: auto;
    position: relative;
  }

  .close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
  }

  .comparison-specs {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid #ddd;
  }

  .spec-row {
    display: grid;
    grid-template-columns: 120px repeat(auto-fit, minmax(120px, 1fr));
    gap: 1px;
    background: #e0e0e0;
  }

  .spec-name {
    background: #f8f8f8;
    padding: 10px;
    font-weight: 600;
    font-size: 12px;
  }

  .spec-value {
    background: white;
    padding: 10px;
    font-size: 12px;
  }

  .phone-header {
    background: #f0f4ff;
    font-weight: 600;
    color: #667eea;
  }

  .phone-checkbox {
    margin: 8px 8px 0 0;
    cursor: pointer;
    width: 18px;
    height: 18px;
  }
'''

# Add CSS before closing </style> tag
content = content.replace('  @media (max-width: 768px) {', css_styles + '\n  @media (max-width: 768px) {')

# Write the updated content back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Comparison feature added successfully!")
print("📊 Users can now select up to 3 phones and compare them side-by-side")
