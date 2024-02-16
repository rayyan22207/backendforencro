from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, FriendRequest, CustomUser
from django.contrib import messages
from direct.models import *
from django.db import transaction

@login_required
def profile_view(request, username):
    user= CustomUser.objects.get(username=username)
    user_profile = Profile.objects.get(user=user.id)
    friend_requests = FriendRequest.objects.filter(to_user=user_profile.user, status='pending')
    context = {
        'user_profile': user_profile,
        'friend_requests': friend_requests,
    }
    return render(request, 'profile.html', context)


@login_required
def send_friend_request(request, username):
    user_to = CustomUser.objects.get(username=username)
    user_from = request.user

    # Check if a friend request already exists or if they are already friends
    existing_request = FriendRequest.objects.filter(from_user=user_from, to_user=user_to).first()
    if existing_request:
        messages.warning(request, 'Friend request already sent.')
    elif user_from == user_to:
        messages.warning(request, 'You cannot send a friend request to yourself.')
    else:
        # Create a new friend request
        FriendRequest.objects.create(from_user=user_from, to_user=user_to, status='pending')
        messages.success(request, 'Friend request sent successfully.')

    return redirect('Accounts:profile', username=username)

@login_required
def friend_requests_view(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'follow.html', context)



@login_required
def respond_to_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if request.user != friend_request.to_user:  # Access the associated user directly
        messages.error(request, "You can't respond to this friend request.")
        return redirect('Accounts:friend_requests')

    if action == 'accept':
        # Check if they were already friends
        if friend_request.to_user.profile.Used_to_be_Friends.filter(id=friend_request.from_user.id).exists():
            # Remove from Used to be Friends
            friend_request.to_user.profile.Used_to_be_Friends.remove(friend_request.from_user)
            # Add to Friends
            friend_request.to_user.profile.Friends.add(friend_request.from_user)
        else:
            # Accept the friend request
            friend_request.status = 'accepted'
            friend_request.save()
            profile_from = friend_request.from_user.profile
            profile_to = friend_request.to_user.profile

            # Add the user who sent the request to your friends
            friend_request.to_user.profile.Friends.add(profile_from)
            friend_request.from_user.profile.Friends.add(profile_to)
            
            # Create a chat room with a UUID
            chat_room, created = OneToOneChat.objects.get_or_create()
            chat_room.participants.set([friend_request.to_user, friend_request.from_user])

            messages.success(request, 'Friend request accepted.')

    elif action == 'decline':
        # Decline the friend request
        friend_request.status = 'declined'
        friend_request.save()
        messages.success(request, 'Friend request declined.')
    else:
        messages.error(request, "Invalid action.")

    return redirect('Accounts:friend_requests')

@login_required
def block(request, username):
    # Get the user you want to block
    user_to_block = User.objects.get(username=username)
    
    if user_to_block == request.user:
        messages.error(request, "You cannot block yourself.")
    else:
        # Remove from Friends
        request.user.profile.Friends.remove(user_to_block)
        # Add to Used to be Friends
        request.user.profile.Used_to_be_Friends.add(user_to_block)
        request.user.profile.Blocked_Friends.add(user_to_block)
        messages.success(request, f"You have blocked {user_to_block.username}.")
    
    return redirect('Accounts:profile', username=username)