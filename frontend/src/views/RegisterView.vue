# frontend/src/views/RegisterView.vue
<template>
  <div class="flex-grow flex items-center justify-center bg-gray-900">
    <div class="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-white mb-6 text-center">Register</h1>

      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label for="username" class="block text-gray-300 text-sm font-bold mb-2">Username:</label>
          <input
            type="text"
            id="username"
            v-model="username"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
            required
          />
        </div>
        <div class="mb-4">
          <label for="email" class="block text-gray-300 text-sm font-bold mb-2">Email:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-300 text-sm font-bold mb-2">Password:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
            required
          />
        </div>

        <p v-if="error" class="text-red-500 text-sm italic mb-4 text-center">{{ error }}</p>

        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
          >
            Register
          </button>
          <router-link to="/login" class="inline-block align-baseline font-bold text-sm text-green-400 hover:text-green-200">
            Already have an account? Login
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const username = ref('');
const email = ref('');
const password = ref('');
const error = ref('');

const handleRegister = async () => {
  error.value = '';
  const result = await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value,
  });

  if (!result.success) {
    error.value = result.error;
  }
  // Redirection is handled by the authStore action on success (which calls login)
};
</script>

<style scoped>
/* Scoped styles are handled primarily by Tailwind CSS classes */
</style>
