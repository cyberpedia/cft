# frontend/src/stores/challenges.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Import the configured axios instance

export const useChallengeStore = defineStore('challenges', {
  state: () => ({
    challenges: [],
    currentChallenge: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchChallenges() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('challenges/');
        this.challenges = response.data;
      } catch (error) {
        this.error = 'Failed to fetch challenges.';
        console.error('Error fetching challenges:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchChallenge(id) {
      this.loading = true;
      this.error = null;
      this.currentChallenge = null;
      try {
        const response = await api.get(`challenges/${id}/`);
        this.currentChallenge = response.data;
      } catch (error) {
        this.error = `Failed to fetch challenge ${id}.`;
        console.error(`Error fetching challenge ${id}:`, error);
      } finally {
        this.loading = false;
      }
    },

    async submitFlag({ challengeId, flag }) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.post(`challenges/${challengeId}/submit/`, { flag });
        // Optionally, refetch challenges or update challenge state if needed after submission
        // this.fetchChallenges(); // or update currentChallenge details
        return { success: true, data: response.data };
      } catch (error) {
        let errorMessage = 'Flag submission failed.';
        if (error.response && error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.message) {
          errorMessage = error.message;
        }
        this.error = errorMessage;
        console.error('Error submitting flag:', error);
        return { success: false, error: errorMessage };
      } finally {
        this.loading = false;
      }
    },
  },
});
