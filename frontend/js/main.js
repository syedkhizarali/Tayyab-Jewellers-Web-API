// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initModals();
    initProfile();
    initWishlist();
    initCart();

    // Check authentication status
    checkAuthStatus();

    // Load initial data
    if (document.getElementById('featuredProducts')) {
        loadFeaturedProducts();
    }

    if (window.location.pathname.includes('products.html')) {
        loadProducts();
    }

    // Load gold rates
    loadGoldRates();
});

// Check authentication status
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userName = document.getElementById('userName');
    const userFullName = document.getElementById('userFullName');
    const userEmail = document.getElementById('userEmail');

    if (token) {
        // Parse JWT token to get user info (in a real app, you'd verify this on backend)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const user = payload.sub;

            if (userName) userName.textContent = user.name || 'Account';
            if (userFullName) userFullName.textContent = user.name || 'User';
            if (userEmail) userEmail.textContent = user.email || '';

            // Update member since
            const memberSince = document.getElementById('memberSince');
            if (memberSince && user.created_at) {
                memberSince.textContent = new Date(user.created_at).getFullYear();
            }
        } catch (e) {
            console.error('Error parsing token:', e);
        }
    }
}

// Initialize navbar functionality
function initNavbar() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.querySelector('.nav-menu');
    const userDropdown = document.querySelector('.user-dropdown');
    const userMenuBtn = document.getElementById('userMenuBtn');

    // Mobile menu toggle
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // User dropdown toggle
    if (userMenuBtn) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('active');
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.user-dropdown')) {
            userDropdown?.classList.remove('active');
        }
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                dropdown.style.opacity = '0';
                dropdown.style.visibility = 'hidden';
            });
        }
    });

    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    const sidebarLogout = document.getElementById('sidebarLogout');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    if (sidebarLogout) {
        sidebarLogout.addEventListener('click', handleLogout);
    }
}

// Handle logout
function handleLogout(e) {
    e.preventDefault();

    // Clear local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');

    // Redirect to home page
    window.location.href = 'index.html';
}

// Initialize modals
function initModals() {
    const modals = document.querySelectorAll('.modal');
    const closeModalBtns = document.querySelectorAll('.close-modal');

    // Close modal on X click
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            modal.classList.remove('active');
        });
    });

    // Close modal when clicking outside
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    // ESC key to close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modals.forEach(modal => modal.classList.remove('active'));
        }
    });
}

// Initialize profile functionality
function initProfile() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const saveProfileBtn = document.getElementById('saveProfileBtn');
    const changePasswordLink = document.getElementById('changePasswordLink');
    const passwordModal = document.getElementById('passwordModal');

    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', () => {
            enableProfileEdit(true);
        });
    }

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', () => {
            enableProfileEdit(false);
            loadProfileData(); // Reload original data
        });
    }

    if (saveProfileBtn) {
        saveProfileBtn.addEventListener('click', (e) => {
            e.preventDefault();
            saveProfile();
        });
    }

    if (changePasswordLink) {
        changePasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            passwordModal.classList.add('active');
        });
    }

    // Password form submission
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', (e) => {
            e.preventDefault();
            changePassword();
        });
    }
}

// Enable/disable profile edit mode
function enableProfileEdit(enabled) {
    const inputs = document.querySelectorAll('#profileForm input:not([type="radio"])');
    const radioInputs = document.querySelectorAll('#profileForm input[type="radio"]');
    const editBtn = document.getElementById('editProfileBtn');
    const cancelBtn = document.getElementById('cancelEditBtn');
    const saveBtn = document.getElementById('saveProfileBtn');

    inputs.forEach(input => {
        input.disabled = !enabled;
    });

    radioInputs.forEach(input => {
        input.disabled = !enabled;
    });

    if (enabled) {
        editBtn.style.display = 'none';
        cancelBtn.style.display = 'block';
        saveBtn.style.display = 'block';
    } else {
        editBtn.style.display = 'block';
        cancelBtn.style.display = 'none';
        saveBtn.style.display = 'none';
    }
}

// Load profile data
async function loadProfileData() {
    try {
        const response = await fetch('http://localhost:8000/api/users/me', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            const user = await response.json();

            // Update form fields
            document.getElementById('profileName').value = user.name || '';
            document.getElementById('profileEmail').value = user.email || '';
            document.getElementById('profilePhone').value = user.phone || '';

            // Update user display
            document.getElementById('userFullName').textContent = user.name || 'User';
            document.getElementById('userName').textContent = user.name || 'Account';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Save profile
async function saveProfile() {
    const formData = {
        name: document.getElementById('profileName').value,
        phone: document.getElementById('profilePhone').value,
        dob: document.getElementById('profileDob').value,
        gender: document.querySelector('input[name="gender"]:checked')?.value
    };

    try {
        const response = await fetch('http://localhost:8000/api/users/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Profile updated successfully!');
            enableProfileEdit(false);
            loadProfileData(); // Reload updated data
        } else {
            throw new Error('Failed to update profile');
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        alert('Error updating profile. Please try again.');
    }
}

// Change password
async function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        alert('New passwords do not match!');
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/api/users/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
                old_password: currentPassword,
                new_password: newPassword
            })
        });

        if (response.ok) {
            alert('Password changed successfully!');
            document.getElementById('passwordModal').classList.remove('active');
            document.getElementById('passwordForm').reset();
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to change password');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        alert(error.message);
    }
}

// Load gold rates
async function loadGoldRates() {
    try {
        const response = await fetch('http://localhost:8000/api/gold-rates/latest');
        if (response.ok) {
            const rates = await response.json();
            updateGoldRatesUI(rates);
        }
    } catch (error) {
        console.error('Error loading gold rates:', error);
    }
}

// Update gold rates in UI
function updateGoldRatesUI(rates) {
    rates.forEach(rate => {
        const element = document.getElementById(`rate${rate.karat}k`);
        if (element) {
            element.textContent = rate.price_per_tola.toLocaleString();
        }
    });

    // Update current gold rate in hero
    const currentRate = document.getElementById('currentGoldRate');
    if (currentRate && rates.length > 0) {
        const rate24k = rates.find(r => r.karat === 24);
        if (rate24k) {
            currentRate.textContent = `PKR ${rate24k.price_per_tola.toLocaleString()}/tola`;
        }
    }

    // Update time
    const updateTime = document.getElementById('updateTime');
    if (updateTime) {
        updateTime.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}

// Initialize wishlist
function initWishlist() {
    updateWishlistCount();
}

// Update wishlist count
async function updateWishlistCount() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        const response = await fetch('http://localhost:8000/api/wishlist', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const wishlist = await response.json();
            const wishlistCount = document.getElementById('wishlistCount');
            if (wishlistCount) {
                wishlistCount.textContent = wishlist.length;
            }
        }
    } catch (error) {
        console.error('Error loading wishlist:', error);
    }
}

// Initialize cart
function initCart() {
    updateCartCount();
}

// Update cart count
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

// Load featured products
async function loadFeaturedProducts() {
    try {
        const response = await fetch('http://localhost:8000/api/products?limit=4');
        if (response.ok) {
            const products = await response.json();
            displayFeaturedProducts(products);
        }
    } catch (error) {
        console.error('Error loading featured products:', error);
    }
}

// Display featured products
function displayFeaturedProducts(products) {
    const container = document.getElementById('featuredProducts');
    if (!container) return;

    container.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.images ? JSON.parse(product.images)[0] : 'assets/images/product-placeholder.jpg'}" alt="${product.name}">
                <button class="wishlist-btn" data-product-id="${product.id}">
                    <i class="far fa-heart"></i>
                </button>
            </div>
            <div class="product-info">
                <h3 class="product-title">${product.name}</h3>
                <div class="product-meta">
                    <span class="product-karat">${product.karat}K</span>
                    <span class="product-weight">${product.weight_grams}g</span>
                </div>
                <div class="product-price">
                    PKR ${product.price.toLocaleString()}
                </div>
                <div class="product-actions">
                    <a href="product-details.html?id=${product.id}" class="btn btn-sm btn-outline">View Details</a>
                    <button class="btn btn-sm btn-primary add-to-cart" data-product-id="${product.id}">Add to Cart</button>
                </div>
            </div>
        </div>
    `).join('');
}