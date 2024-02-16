import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from django.core import serializers
from Accounts.models import Profile
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

#ONETONE
@database_sync_to_async
def get_or_create_chat(room_name):
    chat, created = OneToOneChat.objects.get_or_create(id=room_name)
    return chat

@database_sync_to_async
def save_message(sender, content, chat):
    message = OTOMessage(sender=sender, content=content)
    message.save()
    chat.messages.add(message)
    
@database_sync_to_async
def get_profile(sender):
    return Profile.objects.get(user=sender)

# GROUP CHAT
@database_sync_to_async
def get_or_create_Groupchat(room_name):
    chat, created = GroupChat.objects.get_or_create(name=room_name)
    return chat

@database_sync_to_async
def g_save_message(sender, content, chat):
    message = GroupMessage(sender=sender, content=content)
    message.save()
    chat.messages.add(message)

class OneToOneChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['uuid']

        chat = await get_or_create_chat(self.room_name)

        if not chat:
            await self.close()
            return

        # Initialize room_group_name to None
        self.room_group_name = f"chat_{self.room_name}"

        if await self.authenticate_user():
            

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        sender = self.scope['user']
        chat = await get_or_create_chat(self.room_name)

        if not chat:
            await self.close()
            return
        profile = await get_profile(sender)
        profile_pic = profile.profile_pic
        await save_message(sender=sender, content=message_content, chat=chat)
        print(sender, sender.username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender.username,
                'senderID': sender.id,
                'sender_pfp': profile_pic.url
            }
        )
        

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        senderID = event['senderID']
        sender_pfp = event['sender_pfp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'senderID': senderID,
            'sender_pfp': sender_pfp
        }))
        
    @database_sync_to_async
    def authenticate_user(self):
        # Extract token from scope
        try:
            token_key = self.scope["query_string"].decode("utf-8").split("=")[1]
        except IndexError:
            return False

        # Authenticate user using the token
        try:
            token = Token.objects.get(key=token_key)
            self.scope['user'] = token.user
            return True
        except Token.DoesNotExist:
            return False

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['uuid']

        chat = await get_or_create_chat(self.room_name)

        if not chat:
            await self.close()
            return

        # Initialize room_group_name to None
        self.room_group_name = None

        if await self.authenticate_user():
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

            
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        sender = self.scope['user']
        chat = await get_or_create_Groupchat(self.room_name)

        if not chat:
            await self.close()
            return
        profile = await get_profile(sender)
        profile_pic = profile.profile_pic
        await g_save_message(sender=sender, content=message_content, chat=chat)
        print(sender, sender.username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender.username,
                'sender_pfp': profile_pic.url
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_pfp = event['sender_pfp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_pfp': sender_pfp
        }))























class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['uuid']

        chat = await get_or_create_chat(self.room_name)

        if not chat:
            await self.close()
        else:
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            # Respond to the client that we are connected.
            await self.send(text_data=json.dumps({
                'type': 'connection',
                'data': {
                    'message': "Connected"
                }
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']

            # Use this as room name as well
            self.my_name = name


        if eventType == 'call':
            name = text_data_json['data']['name']
            print(f"{self.my_name} is calling {name}")

            # Notify the callee by sending an event to the callee's group name
            await self.channel_layer.group_send(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # Call has been received, notify the calling user
            caller = text_data_json['data']['caller']
            print(f"{self.my_name} is answering {caller}'s call.")

            await self.channel_layer.group_send(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':
            user = text_data_json['data']['user']

            await self.channel_layer.group_send(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

    async def call_received(self, event):
        print(f'Call received by {self.my_name}')
        await self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))

    async def call_answered(self, event):
        print(f"{self.my_name}'s call answered")
        await self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))

    async def ICEcandidate(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))
