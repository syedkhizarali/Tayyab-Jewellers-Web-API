// Addresses API calls
const API_BASE_URL = 'http://localhost:8000/api';

// Get all addresses
async function getAddresses() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch addresses');
        }

        return await response.json();
    } catch (error) {
        console.error('Addresses fetch error:', error);
        return [];
    }
}

// Get single address
async function getAddress(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses/${id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch address');
        }

        return await response.json();
    } catch (error) {
        console.error('Address fetch error:', error);
        throw error;
    }
}

// Create new address
async function createAddress(addressData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(addressData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create address');
        }

        return await response.json();
    } catch (error) {
        console.error('Address creation error:', error);
        throw error;
    }
}

// Update address
async function updateAddress(id, addressData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses/${id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(addressData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update address');
        }

        return await response.json();
    } catch (error) {
        console.error('Address update error:', error);
        throw error;
    }
}

// Delete address
async function deleteAddress(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to delete address');
        }

        return { success: true };
    } catch (error) {
        console.error('Address deletion error:', error);
        throw error;
    }
}

// Set default address
async function setDefaultAddress(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/addresses/${id}/set-default`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to set default address');
        }

        return await response.json();
    } catch (error) {
        console.error('Set default address error:', error);
        throw error;
    }
}

// Export functions
window.addressesAPI = {
    getAddresses,
    getAddress,
    createAddress,
    updateAddress,
    deleteAddress,
    setDefaultAddress
};