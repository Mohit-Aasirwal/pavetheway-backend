import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

class ResumeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from query string (e.g., ws://localhost:8000/ws/resume/?token=your_token)
        query_string = self.scope['query_string'].decode()
        token_key = None
        for param in query_string.split('&'):
            if param.startswith('token='):
                token_key = param.split('=')[1]
        
        if not token_key:
            await self.close()
            return

        # Validate token
        user = await self.get_user_from_token(token_key)
        if not user:
            await self.close()
            return

        self.user = user
        self.group_name = f'resume_{self.user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send initial data
        resume = await self.get_resume()
        from .serializers import ResumeSerializer  # Import here
        serializer = ResumeSerializer(resume)
        await self.send(text_data=json.dumps({'data': serializer.data}))

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def get_resume(self):
        from .models import Resume  # Import here
        resume, _ = Resume.objects.get_or_create(user=self.user)
        return resume

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def resume_update(self, event):
        await self.send(text_data=json.dumps({'data': event['data']}))