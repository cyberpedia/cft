# frontend/src/services/websocket.js
import ReconnectingWebSocket from 'reconnecting-websocket';

// WebSocket URL for the activity feed
// Use 'ws' for http and 'wss' for https
const WS_URL = 'ws://127.0.0.1:8000/ws/activity/'; 

// Create a ReconnectingWebSocket instance
const ws = new ReconnectingWebSocket(WS_URL);

// Array to store callback functions for messages
const messageListeners = [];

ws.onopen = () => {
  console.log('WebSocket connection opened.');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // console.log('WebSocket message received:', data);
  // Notify all registered listeners
  messageListeners.forEach(listener => listener(data));
};

ws.onclose = (event) => {
  console.log('WebSocket connection closed:', event.code, event.reason);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

export default {
  /**
   * Registers a callback function to be called when a new message is received.
   * @param {function} listener - The callback function that receives the message data.
   */
  onMessage(listener) {
    if (typeof listener === 'function') {
      messageListeners.push(listener);
    }
  },

  /**
   * Unregisters a callback function.
   * @param {function} listener - The callback function to remove.
   */
  offMessage(listener) {
    const index = messageListeners.indexOf(listener);
    if (index > -1) {
      messageListeners.splice(index, 1);
    }
  },

  /**
   * Manually send a message through the websocket.
   * (Not strictly needed for this activity feed which is server-push only, but good for completeness)
   * @param {object} message - The message object to send.
   */
  send(message) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not open. Message not sent:', message);
    }
  },

  /**
   * Closes the WebSocket connection.
   */
  close() {
    ws.close();
  },

  /**
   * Returns the current state of the WebSocket connection.
   * @returns {number} The readyState of the WebSocket.
   */
  get readyState() {
    return ws.readyState;
  },

  /**
   * Returns the WebSocket instance.
   * Useful for directly attaching event handlers if needed.
   */
  get instance() {
    return ws;
  }
};```

```vue
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
