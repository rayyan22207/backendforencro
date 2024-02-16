# imports
from rest_framework import serializers
from django.contrib.auth import get_user_model
from Accounts.models import Profile, FriendRequest, UserSetting
from direct.models import GroupCall, GroupMessage, GroupChat, OneToOneChat, OTOCall, OTOMessage
CustomUser = get_user_model()


        
class UsersmallDetail(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email','username')

class FriendRequestSerializer(serializers.ModelSerializer):
    user = UsersmallDetail()
    class Meta:
        model = FriendRequest
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    #status_set = StatusModelSerializer(many=True, read_only=True)
    user = UsersmallDetail()
    sent_requests = FriendRequestSerializer(many=True, read_only=True)
    received_requests = FriendRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    sent_requests = FriendRequestSerializer(many=True, read_only=True)
    received_requests = FriendRequestSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','username','first_name','last_name', 'username', 'password')  # Include other fields as needed
        extra_kwargs = {'password': {'write_only': True}}

class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = '__all__'
        



        
class GroupChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GroupChat
        fields = '__all__'

class GroupCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCall
        fields = '__all__'

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = '__all__'



class OneToOneCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTOCall
        fields = '__all__'

class ChatResponseSerializer(serializers.Serializer):
    room_name = serializers.UUIDField(allow_null=True)
    


        
class UserForOtOchat(serializers.ModelSerializer):
    profile =ProfileSerializer()
    class Meta:
        model = CustomUser
        fields = ('id','email','username', 'profile')
    

class OTOMessageSerializer(serializers.ModelSerializer):
    sender = UserForOtOchat()
    class Meta:
        model = OTOMessage
        fields = '__all__'
class OneToOneChatSerializer(serializers.ModelSerializer):
    participants = UserForOtOchat(many=True)  # Assuming participants is a ManyToMany field
    messages = OTOMessageSerializer(many=True)

    class Meta:
        model = OneToOneChat
        fields ='__all__'

    

class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'last_activity']