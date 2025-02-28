import { signal, effect } from 'svelte';
import { browser } from '$app/environment';

const defaultValue = {
    token: null,
    isAuthenticated: false,
    user: null
};

// Initialize from localStorage if available
const initialValue = browser 
    ? JSON.parse(localStorage.getItem('auth')) || defaultValue 
    : defaultValue;

// export const auth = signal(initialValue);

// Subscribe to changes and update localStorage
if (browser) {
    effect(() => {
        localStorage.setItem('auth', JSON.stringify(auth()));
    });
}

// Helper functions
export function login(token, user) {
    auth.set({
        token,
        isAuthenticated: true,
        user
    });
}

export function logout() {
    auth.set(defaultValue);
} 