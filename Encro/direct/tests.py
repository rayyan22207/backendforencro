
from .models import OneToOneChat
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.
user1 = User.objects.get(id=1)  # Replace with how you retrieve your users
user2 = User.objects.get(id=2)  # Replace with how you retrieve your users

chat = OneToOneChat.get_chat_between_users(user1, user2)

if chat:
    # You have the chat instance
    chat_id = chat.id
    print(chat_id)
else:
    # No chat exists between these users
    chat_id = None
    print('None')
