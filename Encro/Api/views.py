from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from Accounts.models import CustomUser, Profile, FriendRequest #StatusModel
from .serializers import (
    CustomUserSerializer, 
    ProfileSerializer, 
    CustomUserRegistrationSerializer,
    ChatResponseSerializer,
    GroupChatSerializer, 
    GroupCallSerializer, 
    GroupMessageSerializer, 
    OneToOneChatSerializer, 
    OneToOneCallSerializer, 
    OTOMessageSerializer,
    ActiveUserSerializer
)
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from direct.models import OneToOneChat
from django.shortcuts import get_object_or_404
from direct.models import GroupChat, GroupCall, GroupMessage, OneToOneChat, OTOCall, OTOMessage
from django.db.models import Q
User = get_user_model()
#Logs in
class CustomAuthToken(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in using Django's authentication system
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#signs up
class CustomUserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print('here saving')
            user = serializer.save()
            print('done')

            # Log in the user and obtain a token
            token, _ = Token.objects.get_or_create(user=user)
            print(token)
            return Response(
                {
                    'message': 'User registered successfully',
                    'token': token.key  # Include the token in the response
                },
                status=status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class SearchUser(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        text = self.request.query_params.get('query', None)
        if not text:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(Q(username__icontains=text) | Q(email__icontains=text))


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRequest_UserListCreateView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to include only GroupChat objects related to the requesting user.
        user = self.request.user  # Get the requesting user
        return Profile.objects.filter(user=user)

class CustomUserRequest_UserListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # Filter the queryset to include only GroupChat objects related to the requesting user.
        user = self.request.user.username  # Get the requesting user
        return CustomUser.objects.filter(username=user)
    # views.py







###############profile#######################
#profile request, block, retrict and stuff
# serializing
def serialize_user(user):
    return{
        'user': user.username,
        'user_pfp': user.profile.profile_pic.url,
        'user_id': user.id,
        'user_email': user.email,
    }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_user(request):
    return Response(serialize_user(request.user))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gEt_user(request, pk):
    user = CustomUser.objects.get(id=pk)
    return Response(serialize_user(user))

def serialize_friend_request(friend_request):
    return {
        'id': friend_request.id,
        'from_user': friend_request.from_user.username,
        'to_user': friend_request.to_user.username,
        'status': friend_request.status,
        # Add other fields you want to include
    }
    
def serialize_profile(profile):
    return {
        'user_id': profile.user.id,
        'username': profile.user.username,
        'bio': profile.bio,
        'name': profile.Name,
        #'hobbies': profile.get_hobbies_display(),  # To get the human-readable hobby choice
        # Add other fields as needed
    }

# views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, username):
    user = get_user(username)
    user_profile = Profile.objects.get(user=user)
    friend_requests = FriendRequest.objects.filter(to_user=user_profile.user, status='pending')
    data = {
        'requesting_user': serialize_user(request.user),
        'user_profile': serialize_profile(user_profile),
        'friend_requests': [serialize_friend_request(fr) for fr in friend_requests],
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, username):
    user_to = get_user(username)
    user_from = request.user

    existing_request = FriendRequest.objects.filter(from_user=user_from, to_user=user_to).first()
    if existing_request:
        return Response({'message': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
    elif user_from == user_to:
        return Response({'message': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        FriendRequest.objects.create(from_user=user_from, to_user=user_to, status='pending')
        return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_view(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    data = {
        'requesting_user': serialize_user(request.user),
        'received_requests': [serialize_friend_request(fr) for fr in received_requests],
        'sent_requests': [serialize_friend_request(fr) for fr in sent_requests],
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def respond_to_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if request.user != friend_request.to_user:
        return Response({"detail": "You can't respond to this friend request."}, status=status.HTTP_400_BAD_REQUEST)

    if action == 'accept':
        if friend_request.to_user.profile.Used_to_be_Friends.filter(id=friend_request.from_user.id).exists():
            friend_request.to_user.profile.Used_to_be_Friends.remove(friend_request.from_user.profile)
            friend_request.to_user.profile.Friends.add(friend_request.from_user.profile)
        else:
            friend_request.status = 'accepted'
            friend_request.save()
            profile_from = friend_request.from_user.profile
            profile_to = friend_request.to_user.profile
            friend_request.to_user.profile.Friends.add(profile_from)
            friend_request.from_user.profile.Friends.add(profile_to)
            chat_room = OneToOneChat.objects.create()
            chat_room.participants.set([friend_request.to_user.id, friend_request.from_user.id])
        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
    elif action == 'decline':
        friend_request.status = 'declined'
        friend_request.save()
        return Response({'message': 'Friend request declined.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def block(request, username):
    user_to_block = get_user(username)
    if user_to_block == request.user:
        return Response({'error': 'You cannot block yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        request.user.profile.Friends.remove(user_to_block.profile)
        request.user.profile.Used_to_be_Friends.add(user_to_block.profile)
        request.user.profile.Blocked_Friends.add(user_to_block.profile)
        return Response({'message': f'You have blocked {user_to_block.username}.'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_relationships(request):
    user_profile = Profile.objects.get(user=request.user)

    # Fetch lists of friends, blocked, and restricted users
    friends = user_profile.Friends.all()
    blocked_users = user_profile.Blocked_Friends.all()
    restricted_users = user_profile.Restriced_Friends.all()
    
    data = {
        'friends': [serialize_user(user.user) for user in friends],
        'blocked_users': [serialize_user(user.user) for user in blocked_users],
        'restricted_users': [serialize_user(user.user) for user in restricted_users],
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unblock_user(request, username):
    user_to_unblock = get_user(username)
    user_profile = Profile.objects.get(user=request.user)

    # Check if the user is in the Blocked_Friends list and unblock them
    if user_to_unblock.profile in user_profile.Blocked_Friends.all():
        user_profile.Blocked_Friends.remove(user_to_unblock.profile)
        user_profile.save()
        return Response({'message': f'You have unblocked {user_to_unblock.username}'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': f'{user_to_unblock.username} is not blocked.'}, status=status.HTTP_400_BAD_REQUEST)


def get_user(username):
    return get_object_or_404(CustomUser, username=username)


# CHAT VIEWS
class OneToOneChatAPI(APIView):
    def get(self, request, username):
        User = get_user_model()
        user1 = request.user  # The authenticated user (current user)
        user2 = User.objects.get(username=username)

        chat = OneToOneChat.get_chat_between_users(user1, user2)

        if chat:
            # You have the chat instance
            chat_id = chat.id
        else:
            # No chat exists between these users
            chat_id = None

        response_data = {
            'room_name': chat_id
        }
        serializer = ChatResponseSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###############CHATSSSSSSSS
class GroupChatListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to include only GroupChat objects related to the requesting user.
        user = self.request.user  # Get the requesting user
        return GroupChat.objects.filter(participants=user)

    def perform_create(self, serializer):
        # Set the requesting user as a member when creating a new GroupChat
        serializer.save(participants=[self.request.user], admin_users=[self.request.user],root_user=[self.request.user])
    # Add a user to the participants of the group
    def add_user(self, request, pk, user_id):
        group_chat = self.get_object(pk)
        user = User.objects.get(pk=user_id)
        group_chat.participants.add(user)
        group_chat.save()
        return Response(status=status.HTTP_200_OK)

    # Remove a user from the participants of the group
    def remove_user(self, request, pk, user_id):
        group_chat = self.get_object(pk)
        user = User.objects.get(pk=user_id)
        group_chat.participants.remove(user)
        group_chat.save()
        return Response(status=status.HTTP_200_OK)

    # Make a user an admin user of the group
    def make_admin_user(self, request, pk, user_id):
        group_chat = self.get_object(pk)
        user = User.objects.get(pk=user_id)
        group_chat.admin_users.add(user)
        group_chat.save()
        return Response(status=status.HTTP_200_OK)

    # Remove a user as an admin user of the group
    def remove_admin_user(self, request, pk, user_id):
        group_chat = self.get_object(pk)
        user = User.objects.get(pk=user_id)
        group_chat.admin_users.remove(user)
        group_chat.save()
        return Response(status=status.HTTP_200_OK)
    
        
class GroupCallListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupCallSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter the queryset to include only GroupChat objects related to the requesting user.
        user = self.request.user  # Get the requesting user
        return GroupChat.objects.filter(participants=user)

class GroupMessageListCreateView(generics.ListCreateAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class OneToOneChatListCreateView(generics.ListCreateAPIView):
    serializer_class = OneToOneChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        requesting_user = self.request.user
        queryset = OneToOneChat.objects.filter(participants=requesting_user)
        return queryset

class OneToOneCallListCreateView(generics.ListCreateAPIView):
    queryset = OTOCall.objects.all()
    serializer_class = OneToOneCallSerializer
    permission_classes = [permissions.IsAuthenticated]

class OTOMessageListCreateView(generics.ListCreateAPIView):
    queryset = OTOMessage.objects.all()
    serializer_class = OTOMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

class ActiveUsersAPIView(APIView):
    def get(self, request, *args, **kwargs):
        five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
        active_users = get_user_model().objects.filter(last_activity__gte=five_minutes_ago)
        serializer = ActiveUserSerializer(active_users, many=True)
        return Response(serializer.data)