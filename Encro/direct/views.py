from django.shortcuts import render
from .models import *

        
from .models import OneToOneChat
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    
    return render(request, 'home.html', {})

def chat(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })

def otochat(request, username):
    
    User = get_user_model()

    user1 = request.user  # The authenticated user (current user)
    user2 = User.objects.get(username=username)
    
    chat = OneToOneChat.get_chat_between_users(user1, user2)
    
    if chat:
        # You have the chat instance
        chat_id = chat.id
        print(chat_id)
    else:
        # No chat exists between these users
        chat_id = None
        print('None')
    return render(request, 'otochat.html', {
        'room_name': chat_id
    })
    
def otocall(request, username):
    
    User = get_user_model()

    user1 = request.user  # The authenticated user (current user)
    user2 = User.objects.get(username=username)
    
    chat = OneToOneChat.get_chat_between_users(user1, user2)
    
    if chat:
        # You have the chat instance
        chat_id = chat.id
        print(chat_id)
    else:
        # No chat exists between these users
        chat_id = None
        print('None')
    return render(request, 'otocall.html', {
        'room_name': chat_id
    })
    