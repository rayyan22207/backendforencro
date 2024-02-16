from django.urls import re_path
from . import consumers

websocket_urlpatterns =[
    #re_path(r'ws/direct/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/direct/group/(?P<room_name>\w+)/$', consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/direct/(?P<uuid>[^/]+)/$', consumers.OneToOneChatConsumer.as_asgi()),
    re_path(r'ws/direct/call(?P<uuid>[^/]+/$)', consumers.CallConsumer.as_asgi()),

]