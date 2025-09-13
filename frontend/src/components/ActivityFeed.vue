# frontend/src/components/ActivityFeed.vue
<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-xl mb-6">
    <h2 class="text-2xl font-bold text-white mb-4">Live Activity Feed</h2>
    <div v-if="feedMessages.length === 0" class="text-gray-400 text-center">
      No recent activity yet.
    </div>
    <ul v-else class="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
      <li v-for="(activity, index) in feedMessages" :key="index" class="bg-gray-700 p-3 rounded-md flex items-center justify-between">
        <span class="text-gray-300 text-sm">
          <span class="font-semibold text-blue-400">{{ activity.user }}</span> solved
          <span class="font-semibold text-green-400">{{ activity.challenge }}</span> for
          <span class="font-semibold text-yellow-400">{{ activity.points }}</span> points!
        </span>
        <span class="text-gray-500 text-xs ml-4 whitespace-nowrap">
          {{ formatTime(activity.timestamp) }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import websocketService from '@/services/websocket';

const MAX_MESSAGES = 10; // Keep only the last 10 messages
const feedMessages = ref([]);

// Listener function for WebSocket messages
const handleWebSocketMessage = (data) => {
  if (data.type === 'activity_update' && data.message) {
    feedMessages.value.unshift(data.message); // Add new message to the beginning
    if (feedMessages.value.length > MAX_MESSAGES) {
      feedMessages.value.pop(); // Remove the oldest message if over limit
    }
  }
};

const formatTime = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
};

onMounted(() => {
  websocketService.onMessage(handleWebSocketMessage);
});

onUnmounted(() => {
  websocketService.offMessage(handleWebSocketMessage);
  // Optionally, close the connection if this is the only component using it,
  // but for a global activity feed, it might stay open.
  // websocketService.close();
});
</script>

<style scoped>
/* Custom scrollbar for better appearance */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #374151; /* gray-700 */
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #60a5fa; /* blue-400 */
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #3b82f6; /* blue-500 */
}
</style>
