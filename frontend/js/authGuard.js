// Authentication guard for protected pages
document.addEventListener('DOMContentLoaded', function() {
    // Pages that require authentication
    const protectedPages = [
        'profile.html',
        'addresses.html',
        'wishlist.html',
        'orders.html',
        'checkout.html'
    ];

    // Get current page
    const currentPage = window.location.pathname.split('/').pop();

    // Check if current page is protected
    if (protectedPages.includes(currentPage)) {
        // Check if user is authenticated
        const token = localStorage.getItem('access_token');

        if (!token) {
            // Redirect to login page
            window.location.href = 'login.html?redirect=' + encodeURIComponent(window.location.pathname);
            return;
        }

        // Verify token (in a real app, you might want to verify with backend)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const expiry = payload.exp * 1000; // Convert to milliseconds

            if (Date.now() > expiry) {
                // Token expired, try to refresh
                refreshToken().then(newToken => {
                    if (!newToken) {
                        // Refresh failed, redirect to login
                        window.location.href = 'login.html?redirect=' + encodeURIComponent(window.location.pathname);
                    }
                });
            }
        } catch (e) {
            // Invalid token, redirect to login
            window.location.href = 'login.html?redirect=' + encodeURIComponent(window.location.pathname);
        }
    }

    // For login/register pages, redirect to profile if already logged in
    if (currentPage === 'login.html' || currentPage === 'register.html') {
        const token = localStorage.getItem('access_token');
        if (token) {
            window.location.href = 'profile.html';
        }
    }
});

// Refresh token function
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return null;

    try {
        const response = await fetch('http://localhost:8000/api/auth/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            return data.access_token;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
    }

    return null;
}