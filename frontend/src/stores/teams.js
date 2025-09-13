# frontend/src/stores/teams.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Import the configured axios instance
import { useAuthStore } from '@/stores/auth'; // To update user's team status

export const useTeamStore = defineStore('teams', {
  state: () => ({
    teams: [],
    currentTeam: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchTeams() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('teams/');
        this.teams = response.data;
      } catch (error) {
        this.error = 'Failed to fetch teams.';
        console.error('Error fetching teams:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchTeam(id) {
      this.loading = true;
      this.error = null;
      this.currentTeam = null;
      try {
        const response = await api.get(`teams/${id}/`);
        this.currentTeam = response.data;
      } catch (error) {
        this.error = `Failed to fetch team ${id}.`;
        console.error(`Error fetching team ${id}:`, error);
      } finally {
        this.loading = false;
      }
    },

    async createTeam(name) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      try {
        const response = await api.post('teams/', { name });
        // Update user's team status in auth store
        authStore.user.team = response.data.id; // Assuming API returns the created team's ID
        authStore.setUser(authStore.user);
        this.currentTeam = response.data; // Also update currentTeam for immediate display
        this.fetchTeams(); // Refresh the list of all teams
        return { success: true, data: response.data };
      } catch (error) {
        let errorMessage = 'Failed to create team.';
        if (error.response && error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response && error.response.data && error.response.data.name) {
          errorMessage = `Name: ${error.response.data.name.join(', ')}`;
        }
        this.error = errorMessage;
        console.error('Error creating team:', error);
        return { success: false, error: errorMessage };
      } finally {
        this.loading = false;
      }
    },

    async joinTeam(id) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      try {
        const response = await api.post(`teams/${id}/join/`);
        // Update user's team status in auth store
        authStore.user.team = id;
        authStore.setUser(authStore.user);
        this.fetchTeam(id); // Fetch the newly joined team's details
        this.fetchTeams(); // Refresh the list of all teams
        return { success: true, data: response.data };
      } catch (error) {
        let errorMessage = 'Failed to join team.';
        if (error.response && error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        }
        this.error = errorMessage;
        console.error('Error joining team:', error);
        return { success: false, error: errorMessage };
      } finally {
        this.loading = false;
      }
    },

    async leaveTeam() {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      try {
        const response = await api.post('teams/leave/');
        // Clear user's team status in auth store
        authStore.user.team = null;
        authStore.setUser(authStore.user);
        this.currentTeam = null; // Clear current team from store
        this.fetchTeams(); // Refresh the list of all teams
        return { success: true, data: response.data };
      } catch (error) {
        let errorMessage = 'Failed to leave team.';
        if (error.response && error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        }
        this.error = errorMessage;
        console.error('Error leaving team:', error);
        return { success: false, error: errorMessage };
      } finally {
        this.loading = false;
      }
    },
  },
});
