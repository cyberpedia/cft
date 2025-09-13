# frontend/src/views/TeamsView.vue
<template>
  <div class="container mx-auto p-6">
    <h1 class="text-4xl font-bold text-white mb-8 text-center">Teams</h1>

    <div v-if="teamStore.loading" class="text-center text-gray-400 mb-4">Loading teams data...</div>
    <div v-if="teamStore.error" class="text-center text-red-500 mb-4">{{ teamStore.error }}</div>
    <div v-if="generalMessage" :class="generalMessageSuccess ? 'text-green-500' : 'text-red-500'" class="mb-4 text-center">
        {{ generalMessage }}
    </div>

    <!-- User is on a team -->
    <div v-if="authStore.user?.team && teamStore.currentTeam" class="bg-gray-800 rounded-lg shadow-xl p-8 max-w-2xl mx-auto">
      <h2 class="text-3xl font-semibold text-blue-400 mb-4">Your Team: {{ teamStore.currentTeam.name }}</h2>
      <p class="text-gray-300 mb-4">Created At: {{ new Date(teamStore.currentTeam.created_at).toLocaleString() }}</p>
      
      <h3 class="text-2xl font-semibold text-white mb-3">Members:</h3>
      <ul class="list-disc list-inside text-gray-300 mb-6">
        <li v-for="member in teamStore.currentTeam.members" :key="member.id">
          {{ member.username }} (Score: {{ member.score }})
        </li>
      </ul>

      <button
        @click="handleLeaveTeam"
        class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
        :disabled="teamStore.loading"
      >
        Leave Team
      </button>
    </div>

    <!-- User is NOT on a team -->
    <div v-else class="max-w-4xl mx-auto">
      <div class="bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
        <h2 class="text-3xl font-semibold text-green-400 mb-4 text-center">Create a New Team</h2>
        <form @submit.prevent="handleCreateTeam" class="flex flex-col gap-4">
          <input
            type="text"
            v-model="newTeamName"
            placeholder="Enter new team name"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
            required
          />
          <button
            type="submit"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded focus:outline-none focus:shadow-outline transition duration-200"
            :disabled="teamStore.loading"
          >
            Create Team
          </button>
        </form>
      </div>

      <div class="bg-gray-800 rounded-lg shadow-xl p-8">
        <h2 class="text-3xl font-semibold text-purple-400 mb-6 text-center">Join an Existing Team</h2>
        <div v-if="teamStore.teams.length === 0" class="text-center text-gray-400">No other teams to join.</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="team in teamStore.teams"
            :key="team.id"
            class="bg-gray-700 rounded-lg shadow-md p-4 flex flex-col justify-between"
          >
            <h3 class="text-xl font-semibold text-white mb-2">{{ team.name }}</h3>
            <button
              @click="handleJoinTeam(team.id)"
              class="mt-auto bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
              :disabled="teamStore.loading"
            >
              Join Team
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTeamStore } from '@/stores/teams';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const teamStore = useTeamStore();

const { user } = storeToRefs(authStore);
const { teams, currentTeam } = storeToRefs(teamStore);

const newTeamName = ref('');
const generalMessage = ref('');
const generalMessageSuccess = ref(false);

const updateTeamView = async () => {
    generalMessage.value = '';
    if (user.value?.team) {
        await teamStore.fetchTeam(user.value.team);
    } else {
        teamStore.currentTeam = null; // Clear current team state if user has no team
        await teamStore.fetchTeams();
    }
};

onMounted(() => {
    updateTeamView();
});

// Watch for changes in the user's team status
watch(() => user.value?.team, (newTeamId, oldTeamId) => {
    if (newTeamId !== oldTeamId) {
        updateTeamView();
    }
}, { immediate: true }); // Run immediately on component mount

const handleCreateTeam = async () => {
  generalMessage.value = '';
  const result = await teamStore.createTeam(newTeamName.value);
  if (result.success) {
    generalMessage.value = `Successfully created and joined team '${newTeamName.value}'.`;
    generalMessageSuccess.value = true;
    newTeamName.value = ''; // Clear form
  } else {
    generalMessage.value = result.error;
    generalMessageSuccess.value = false;
  }
};

const handleJoinTeam = async (teamId) => {
  generalMessage.value = '';
  const result = await teamStore.joinTeam(teamId);
  if (result.success) {
    generalMessage.value = result.data.detail || 'Successfully joined team.';
    generalMessageSuccess.value = true;
  } else {
    generalMessage.value = result.error;
    generalMessageSuccess.value = false;
  }
};

const handleLeaveTeam = async () => {
  generalMessage.value = '';
  const result = await teamStore.leaveTeam();
  if (result.success) {
    generalMessage.value = result.data.detail || 'Successfully left team.';
    generalMessageSuccess.value = true;
  } else {
    generalMessage.value = result.error;
    generalMessageSuccess.value = false;
  }
};
</script>

<style scoped>
/* Tailwind handles most styling */
</style>
