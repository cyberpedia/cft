# frontend/src/services/api.js
import axios from 'axios';
import { useAuthStore } from '@/stores/auth'; // Import the auth store

// Create a global Axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Your Django backend API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add the Authorization header
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const accessToken = authStore.accessToken;

    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling token refreshes (optional for this prompt, but good practice)
// This part is for future extensibility and is not strictly required by the current prompt,
// but it's a common pattern when dealing with JWTs.
// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const authStore = useAuthStore();
//     const originalRequest = error.config;

//     // If the error is 401 Unauthorized and it's not the refresh token endpoint itself
//     if (error.response.status === 401 && !originalRequest._retry && error.response.config.url !== 'token/refresh/') {
//       originalRequest._retry = true;

//       try {
//         const refreshToken = authStore.refreshToken;
//         if (refreshToken) {
//           const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh: refreshToken });
//           const newAccessToken = response.data.access;
//           authStore.setTokens(newAccessToken, refreshToken); // Only access token refreshes
//           originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
//           return api(originalRequest); // Retry the original request with the new token
//         }
//       } catch (refreshError) {
//         // Refresh token failed, log out the user
//         authStore.logout();
//         return Promise.reject(refreshError);
//       }
//     }
//     return Promise.reject(error);
//   }
// );

export default api;
