# frontend/src/views/ChallengesView.vue
<template>
  <div class="container mx-auto p-6">
    <h1 class="text-4xl font-bold text-white mb-8 text-center">Challenges</h1>

    <div v-if="challengeStore.loading" class="text-center text-gray-400">Loading challenges...</div>
    <div v-else-if="challengeStore.error" class="text-center text-red-500">{{ challengeStore.error }}</div>
    <div v-else-if="challengeStore.challenges.length === 0" class="text-center text-gray-400">No challenges available yet.</div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="challenge in challengeStore.challenges"
        :key="challenge.id"
        :to="{ name: 'challenge-detail', params: { id: challenge.id } }"
        class="bg-gray-800 rounded-lg shadow-lg p-6 hover:bg-gray-700 transition-colors duration-200 block"
      >
        <h2 class="text-2xl font-semibold text-blue-400 mb-2">{{ challenge.name }}</h2>
        <p class="text-gray-300 mb-4">{{ challenge.points }} points</p>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in challenge.tags"
            :key="tag.id"
            class="bg-purple-600 text-white text-xs font-semibold px-2.5 py-0.5 rounded-full"
          >
            {{ tag.name }}
          </span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useChallengeStore } from '@/stores/challenges';

const challengeStore = useChallengeStore();

onMounted(() => {
  challengeStore.fetchChallenges();
});
</script>

<style scoped>
/* Scoped styles are handled primarily by Tailwind CSS classes */
</style>
