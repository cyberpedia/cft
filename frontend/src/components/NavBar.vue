# frontend/src/components/NavBar.vue
<template>
  <nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex justify-between items-center">
      <!-- Logo and Home Button -->
      <router-link to="/" class="flex items-center space-x-2 text-white text-2xl font-bold hover:text-blue-400 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-1-3m-6.938-9L2 7v11l4.614-2.023A12.022 12.022 0 0112 10.125c1.794 0 3.528.46 5.093 1.34L22 18V7l-7.75-2.917V2.25L12 3.75 9.75 2.25v2.583z" />
        </svg>
        <span>CTF Platform</span>
      </router-link>

      <!-- Core Pages & User Controls -->
      <div class="flex items-center space-x-6">
        <!-- Links for authenticated users -->
        <template v-if="isAuthenticated">
          <router-link to="/challenges" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Challenges</router-link>
          <router-link to="/leaderboard" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Leaderboard</router-link>
          <router-link to="/teams" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Teams</router-link>
          <router-link to="/rules" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Rules/FAQ</router-link>
          
          <!-- User Profile (with picture/score - placeholder for now) -->
          <div class="relative group">
            <router-link to="/profile" class="flex items-center space-x-2 text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">
              <img src="https://via.placeholder.com/24" alt="User Avatar" class="w-6 h-6 rounded-full border-2 border-gray-400">
              <span>{{ user?.username }} ({{ user?.score }} pts)</span>
            </router-link>
            <!-- Notifications icon (placeholder) -->
            <button class="text-gray-300 hover:text-white p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>
            <!-- Logout Button -->
            <button @click="handleLogout" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium ml-4">Logout</button>
          </div>
        </template>

        <!-- Links for unauthenticated users -->
        <template v-else>
          <router-link to="/login" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Login</router-link>
          <router-link to="/register" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-lg font-medium">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);

const handleLogout = () => {
  authStore.logout();
};
</script>

<style scoped>
/* Tailwind CSS handles most of the styling */
</style>
