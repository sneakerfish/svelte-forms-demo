import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
});

// Add auth token to requests
api.interceptors.request.use(config => {
    const authValue = auth();
    if (authValue.token) {
        config.headers.Authorization = `Bearer ${authValue.token}`;
    }
    return config;
});

// Handle 401 responses
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            auth.set({ token: null, isAuthenticated: false, user: null });
        }
        return Promise.reject(error);
    }
);

export default api; 