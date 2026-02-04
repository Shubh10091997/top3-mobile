// Phone Comparison Feature
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
  if (btn) {
    if (selectedPhones.length >= 2) {
      btn.style.display = 'inline-block';
    } else {
      btn.style.display = 'none';
    }
  }
}

function openComparison() {
  const modal = document.getElementById('comparisonModal');
  const table = document.getElementById('comparisonTable');
  
  if (!modal || !table || selectedPhones.length < 2) return;
  
  let html = '<div class="comparison-specs">';
  const specs = ['price', 'ram', 'processor', 'storage', 'camera', 'battery', 'display', 'gaming', 'camera_score', 'battery_score', 'performance'];
  
  html += '<div class="spec-row spec-header"><div class="spec-name">Specs</div>';
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
  modal.style.display = 'block';
}

function closeComparison() {
  const modal = document.getElementById('comparisonModal');
  if (modal) {
    modal.style.display = 'none';
  }
}
