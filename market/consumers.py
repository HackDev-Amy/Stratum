from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PriceConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("prices", self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard("prices", self.channel_name)
    async def price_update(self, event):
        await self.send_json({"symbol": event["symbol"], "price": event["price"]})