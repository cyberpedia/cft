# frontend/src/views/LeaderboardView.vue
<template>
  <div class="container mx-auto p-6">
    <h1 class="text-4xl font-bold text-white mb-8 text-center">Leaderboard</h1>

    <div v-if="leaderboardStore.loading" class="text-center text-gray-400">Loading leaderboard...</div>
    <div v-else-if="leaderboardStore.error" class="text-center text-red-500">{{ leaderboardStore.error }}</div>
    <div v-else-if="leaderboardStore.rankings.length === 0" class="text-center text-gray-400">No teams on the leaderboard yet.</div>
    
    <div v-else class="overflow-x-auto bg-gray-800 rounded-lg shadow-xl">
      <table class="min-w-full divide-y divide-gray-700">
        <thead class="bg-gray-700">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Rank</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Team Name</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Total Score</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Last Solve Time</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700">
          <tr v-for="(team, index) in leaderboardStore.rankings" :key="team.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{{ index + 1 }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{{ team.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{{ team.total_score }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
              {{ team.last_solve_time ? new Date(team.last_solve_time).toLocaleString() : 'N/A' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useLeaderboardStore } from '@/stores/leaderboard';

const leaderboardStore = useLeaderboardStore();

onMounted(() => {
  leaderboardStore.fetchLeaderboard();
});
</script>

<style scoped>
/* Tailwind handles most styling */
</style>
