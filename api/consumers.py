# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ActivityConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for broadcasting real-time activity (e.g., flag solves).
    Clients connect to 'ws/activity/' and receive updates from the 'activity_feed' group.
    """
    async def connect(self):
        self.group_name = 'activity_feed'

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: {self.channel_name} joined {self.group_name}")

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} left {self.group_name} with code {close_code}")

    # Receive message from room group
    async def feed_message(self, event):
        """
        Receives a 'feed.message' event from the channel layer and sends it to the WebSocket.
        This method name must match the 'type' field in the group_send message (e.g., 'feed.message' calls 'feed_message').
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'activity_update',
            'message': message
        }))
        # print(f"Sent message to WebSocket {self.channel_name}: {message}")

    async def receive(self, text_data=None, bytes_data=None):
        # We don't expect clients to send messages to this consumer,
        # but if they do, we can log it or ignore it.
        # print(f"Received message from WebSocket {self.channel_name}: {text_data}")
        pass
