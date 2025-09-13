# frontend/src/views/ChallengeDetailView.vue
<template>
  <div class="container mx-auto p-6">
    <div v-if="challengeStore.loading" class="text-center text-gray-400">Loading challenge details...</div>
    <div v-else-if="challengeStore.error" class="text-center text-red-500">{{ challengeStore.error }}</div>
    <div v-else-if="!challengeStore.currentChallenge" class="text-center text-gray-400">Challenge not found.</div>

    <div v-else class="bg-gray-800 rounded-lg shadow-xl p-8 max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-blue-400 mb-4">{{ challengeStore.currentChallenge.name }}</h1>
      <p class="text-gray-300 text-xl mb-6">{{ challengeStore.currentChallenge.points }} points</p>

      <div class="mb-6">
        <h2 class="text-2xl font-semibold text-white mb-2">Description</h2>
        <p class="text-gray-300 leading-relaxed" v-html="challengeStore.currentChallenge.description"></p>
      </div>

      <div v-if="challengeStore.currentChallenge.tags && challengeStore.currentChallenge.tags.length" class="mb-6">
        <h2 class="text-2xl font-semibold text-white mb-2">Tags</h2>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in challengeStore.currentChallenge.tags"
            :key="tag.id"
            class="bg-purple-600 text-white text-sm font-semibold px-3 py-1 rounded-full"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>

      <div v-if="challengeStore.currentChallenge.file" class="mb-6">
        <h2 class="text-2xl font-semibold text-white mb-2">Download File</h2>
        <a :href="challengeStore.currentChallenge.file" target="_blank" class="text-green-400 hover:underline">
          Download Challenge File
        </a>
      </div>

      <div v-if="challengeStore.currentChallenge.hints && challengeStore.currentChallenge.hints.length" class="mb-6">
        <h2 class="text-2xl font-semibold text-white mb-2">Hints</h2>
        <ul>
          <li v-for="hint in challengeStore.currentChallenge.hints" :key="hint.id" class="mb-2 text-gray-300">
            <span v-if="hint.is_unlocked">
              Hint (Cost: {{ hint.cost }} pts): {{ hint.text }}
            </span>
            <span v-else>
              Hint (Cost: {{ hint.cost }} pts) - <button @click="unlockHint(hint.id)" class="text-yellow-400 hover:underline">Unlock</button>
            </span>
          </li>
        </ul>
      </div>

      <div class="mt-8 pt-6 border-t border-gray-700">
        <h2 class="text-2xl font-semibold text-white mb-4">Submit Flag</h2>
        <form @submit.prevent="handleFlagSubmission" class="flex gap-4">
          <input
            type="text"
            v-model="submittedFlag"
            placeholder="Enter your flag"
            class="flex-grow shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
            required
          />
          <button
            type="submit"
            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded focus:outline-none focus:shadow-outline transition duration-200"
          >
            Submit
          </button>
        </form>
        <p v-if="submissionMessage" :class="submissionSuccess ? 'text-green-500' : 'text-red-500'" class="mt-4 text-center">
          {{ submissionMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useChallengeStore } from '@/stores/challenges';
import { useAuthStore } from '@/stores/auth'; // Needed for user score, potentially for unlocking hints
import api from '@/services/api'; // Direct API import for hint unlock

const route = useRoute();
const challengeStore = useChallengeStore();
const authStore = useAuthStore(); // For updating user score locally

const submittedFlag = ref('');
const submissionMessage = ref('');
const submissionSuccess = ref(false);

onMounted(() => {
  const challengeId = route.params.id;
  if (challengeId) {
    challengeStore.fetchChallenge(challengeId);
  }
});

const handleFlagSubmission = async () => {
  submissionMessage.value = ''; // Clear previous messages
  const challengeId = route.params.id;
  if (!challengeId || !submittedFlag.value) {
    submissionMessage.value = 'Please enter a flag.';
    submissionSuccess.value = false;
    return;
  }

  const result = await challengeStore.submitFlag({
    challengeId: challengeId,
    flag: submittedFlag.value,
  });

  if (result.success) {
    submissionMessage.value = result.data.detail || 'Flag submitted successfully!';
    submissionSuccess.value = true;
    // Update user's score locally for immediate feedback
    if (authStore.user && result.data.points_awarded) {
        authStore.user.score += result.data.points_awarded;
        authStore.setUser(authStore.user); // Persist updated user object
    }
    // Optionally refetch challenge details to update hints/points, etc.
    challengeStore.fetchChallenge(challengeId);
  } else {
    submissionMessage.value = result.error || 'Failed to submit flag.';
    submissionSuccess.value = false;
  }
};

const unlockHint = async (hintId) => {
    try {
        const response = await api.post(`hints/${hintId}/unlock/`);
        // Update user's score locally
        if (authStore.user && response.data.cost_deducted) {
            authStore.user.score -= response.data.cost_deducted;
            authStore.setUser(authStore.user); // Persist updated user object
        }
        // Refetch challenge to show the unlocked hint text
        challengeStore.fetchChallenge(route.params.id);
        alert(response.data.detail);
    } catch (error) {
        let errorMessage = 'Failed to unlock hint.';
        if (error.response && error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail;
        }
        alert(errorMessage);
        console.error('Error unlocking hint:', error);
    }
};

</script>

<style scoped>
/* Scoped styles are handled primarily by Tailwind CSS classes */
</style>
