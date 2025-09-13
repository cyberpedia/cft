# frontend/src/stores/auth.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Import the configured axios instance
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
    },

    setUser(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },

    async login(credentials) {
      try {
        const tokenResponse = await api.post('token/', credentials);
        this.setTokens(tokenResponse.data.access, tokenResponse.data.refresh);

        // Fetch user profile after successful login
        const userProfileResponse = await api.get('profile/');
        this.setUser(userProfileResponse.data);

        router.push('/'); // Redirect to homepage or challenges
        return { success: true };
      } catch (error) {
        this.logout(); // Clear any partial state if login fails
        let errorMessage = 'Login failed. Please check your credentials.';
        if (error.response && error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.message) {
          errorMessage = error.message;
        }
        return { success: false, error: errorMessage };
      }
    },

    async register(userData) {
      try {
        await api.post('register/', userData);
        // If registration is successful, automatically log in the user
        const loginResult = await this.login({
          username: userData.username,
          password: userData.password,
        });
        return loginResult;
      } catch (error) {
        let errorMessage = 'Registration failed.';
        if (error.response && error.response.data) {
          // Attempt to parse validation errors
          const errors = error.response.data;
          if (errors.username) errorMessage += ` Username: ${errors.username.join(' ')}`;
          if (errors.email) errorMessage += ` Email: ${errors.email.join(' ')}`;
          if (errors.password) errorMessage += ` Password: ${errors.password.join(' ')}`;
          if (errors.detail) errorMessage = errors.detail; // General error detail
        } else if (error.message) {
          errorMessage = error.message;
        }
        return { success: false, error: errorMessage };
      }
    },

    logout() {
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      router.push('/login'); // Redirect to login page after logout
    },
  },
});
