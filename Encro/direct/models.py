from django.db import models
from django.contrib.auth import get_user_model 
import uuid
from django.utils import timezone

User = get_user_model()

# Create your models here.

class OneToOneChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User)
    messages = models.ManyToManyField('OTOMessage', related_name='chat', blank=True)
    
    
    @classmethod
    def get_chat_between_users(cls, user1, user2):
        # Filter chats with exactly two participants, user1 and user2
        chat = cls.objects.filter(participants=user1).filter(participants=user2)

        if chat.exists():
            return chat.first()
        else:
            return None

    
class GroupChat(models.Model):
    root_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_chats_created')
    admin_users = models.ManyToManyField(User, blank=True, default=None, related_name='group_chats_admin')
    participants = models.ManyToManyField(User, related_name='group_chats_participating')
    name = models.CharField(max_length=255, blank=False)
    messages = models.ManyToManyField('GroupMessage', related_name='chat', blank=True)


    def __str__(self):
        return self.name or f"Group Chat {self.name}"

        
class OTOMessage(models.Model):
    # Message model for one-to-one chat
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(default=timezone.now)  # Use default
    content = models.TextField(blank=True, default='')

    def __str__(self):
        return f"OTO Message from {self.sender} at {self.content}"

class GroupMessage(models.Model):
    # Message model for group chat
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(default=timezone.now)  # Use default
    content = models.TextField(blank=True, default='')
    #chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages', default=None)

    def __str__(self):
        return f"Group Message from {self.sender} at {self.timestamp}"
    
class GroupCall(models.Model):
    
    call_start_time = models.DateTimeField(auto_now_add=True)
    call_duration_minutes = models.PositiveIntegerField(default=0)  # Duration in minutes
    is_video_call = models.BooleanField(default=False) 
    
class OTOCall(models.Model):
    call_start_time = models.DateTimeField(auto_now_add=True)
    call_duration_minutes = models.PositiveIntegerField(default=0)  # Duration in minutes
    is_video_call = models.BooleanField(default=False)  # True for video call, False for normal call