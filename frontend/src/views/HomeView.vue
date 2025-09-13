# frontend/src/views/HomeView.vue
<template>
  <div class="container mx-auto p-6">
    <div class="text-center mb-8">
      <h1 class="text-5xl font-bold text-blue-400 mb-4">Welcome to the CTF Platform!</h1>
      <p class="text-xl text-gray-300">Your ultimate destination for Capture The Flag competitions.</p>
      
      <div v-if="authStore.isAuthenticated" class="mt-8">
        <router-link to="/challenges" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg transition duration-200">
          Browse Challenges
        </router-link>
      </div>
      <div v-else class="mt-8">
        <router-link to="/register" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg text-lg transition duration-200 mr-4">
          Get Started
        </router-link>
        <router-link to="/login" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg text-lg transition duration-200">
          Login
        </router-link>
      </div>
    </div>

    <!-- Live Activity Feed -->
    <ActivityFeed />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import ActivityFeed from '@/components/ActivityFeed.vue'; // Import the new component

const authStore = useAuthStore();
</script>

<style scoped>
/* Placeholder for HomeView */
</style>
