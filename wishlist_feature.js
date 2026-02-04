// Wishlist Feature Implementation
// Add this to index.html

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

function isInWishlist(phoneName) {
  return wishlist.includes(phoneName);
}

function updateWishlistUI() {
  const count = document.getElementById('wishlistCount');
  if (count) {
    count.textContent = wishlist.length;
  }
  
  // Update all heart icons
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    const phoneName = btn.dataset.phone;
    if (isInWishlist(phoneName)) {
      btn.classList.add('in-wishlist');
    } else {
      btn.classList.remove('in-wishlist');
    }
  });
}

function viewWishlist() {
  if (wishlist.length === 0) {
    alert('Your wishlist is empty!');
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
          <button class="remove-wishlist" onclick="toggleWishlist('${phone.name}'); updateWishlistUI();">✕</button>
          <h4>${phone.name}</h4>
          <p class="price">₹${phone.price.toLocaleString()}</p>
          <p class="brand">${phone.company || 'Brand'}</p>
          <a href="/compare?phones=${phone.name}" class="compare-link">Compare</a>
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
document.addEventListener('DOMContentLoaded', updateWishlistUI);
