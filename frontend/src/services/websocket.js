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
};
