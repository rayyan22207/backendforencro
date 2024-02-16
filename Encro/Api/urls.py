from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path

from .views import *
from . import views

urlpatterns = [
    path('auth/users/', CustomUserListCreateView.as_view(), name='user-list-create'), # listing all users
    path('auth/users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'), # spesific user
    path('auth/profiles/', ProfileListCreateView.as_view(), name='profile-list-create'), # listing all profiles
    path('auth/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'), # specific profile
    path('auth/register/', CustomUserRegistrationView.as_view(), name='register'),
    path('user_login/',CustomAuthToken.as_view(), name='login'),
    path('auth/users/profile', ProfileRequest_UserListCreateView.as_view(), name='user-profile'),
    path('auth/users/user', CustomUserRequest_UserListCreateView.as_view(), name='user-user'),
    path('auth/users/search', SearchUser.as_view(), name='Search-User'),
    
    #profile

    path('profile/<str:username>/', views.profile_view, name='api-profile'), # only the small details for chat profiles
    path('send_friend_request/<str:username>/', views.send_friend_request, name='api-send-friend-request'), # to send a friend request
    path('friend_requests/', views.friend_requests_view, name='api-friend-requests'), # all the friend requests for the reqeusting user
    path('respond_to_friend_request/<int:request_id>/<str:action>/', views.respond_to_friend_request, name='api-respond-to-friend-request'), # responding to the request
    path('block/<str:username>/', views.block, name='api-block'), # blocking the user
    path('display-relationships/', views.display_relationships, name='display_relationships'), #displays all the blocks, friends, restriced
    path('unblock-user/<str:username>/', views.unblock_user, name='unblock_user'), #to unblock
    
    # CHAT
    path('otochat/<str:username>/', OneToOneChatAPI.as_view(), name='otochat-api'), # peer to peer chats working not for listing but for the chat itself
    path('groupchats/', views.GroupChatListCreateView.as_view(), name='group-chat-list'), # will list the groups in which the requesting user is a member of
    #path('groupcalls/', views.GroupCallListCreateView.as_view(), name='group-call-list'), # will list the calls in which the gcc has the requesting user (NOT WORKING)
    path('groupmessages/', views.GroupMessageListCreateView.as_view(), name='group-message-list'), # will list all the messages of all the groups
    path('onetoonechats/', views.OneToOneChatListCreateView.as_view(), name='one-to-one-chat-list'), #will only list the requesting users chats
    #path('onetoonecalls/', views.OneToOneCallListCreateView.as_view(), name='one-to-one-call-list'), # (NOT WORKING)
    path('onetoonemessages/', views.OTOMessageListCreateView.as_view(), name='one-to-one-message-list'),  # will list all the messages of all the OTOchats
    
    path('request-user/', views.request_user, name='request-user'),
    path('auth/get-user/<int:pk>/', views.gEt_user, name='get-user'),
    
    #tests
    path('active_users/', ActiveUsersAPIView.as_view(), name='active_users_api'),
    
]
