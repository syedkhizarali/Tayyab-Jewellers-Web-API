// Profile API calls
const API_BASE_URL = 'http://localhost:8000/api';

// Update user profile
async function updateProfile(profileData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/profile`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profileData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Update failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Profile update error:', error);
        throw error;
    }
}

// Upload profile picture
async function uploadProfilePicture(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/users/profile/picture`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Profile picture upload error:', error);
        throw error;
    }
}

// Get user statistics
async function getUserStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/stats`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch stats');
        }

        return await response.json();
    } catch (error) {
        console.error('Stats fetch error:', error);
        return { orders: 0, wishlist: 0, addresses: 0 };
    }
}

// Change password
async function changePassword(oldPassword, newPassword) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/change-password`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Password change failed');
        }

        return { success: true };
    } catch (error) {
        console.error('Password change error:', error);
        throw error;
    }
}

// Load user data for profile page
async function loadUserProfile() {
    try {
        const [user, stats] = await Promise.all([
            fetch(`${API_BASE_URL}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            }).then(res => res.json()),
            getUserStats()
        ]);

        return { user, stats };
    } catch (error) {
        console.error('Error loading user profile:', error);
        throw error;
    }
}

// Export functions
window.profileAPI = {
    updateProfile,
    uploadProfilePicture,
    getUserStats,
    changePassword,
    loadUserProfile
};