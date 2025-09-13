# frontend/src/stores/leaderboard.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Import the configured axios instance

export const useLeaderboardStore = defineStore('leaderboard', {
  state: () => ({
    rankings: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchLeaderboard() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('leaderboard/');
        this.rankings = response.data;
      } catch (error) {
        this.error = 'Failed to fetch leaderboard.';
        console.error('Error fetching leaderboard:', error);
      } finally {
        this.loading = false;
      }
    },
  },
});
