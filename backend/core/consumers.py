import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    # Receive message from room group
    async def broadcast_event(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["payload"]))
