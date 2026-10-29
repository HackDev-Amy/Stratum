# consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PortfolioConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4401)
            return
        self.group = f"portfolio_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)
    async def portfolio_update(self, event):
        await self.send_json(event)