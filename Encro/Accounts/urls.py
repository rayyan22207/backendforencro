from django.urls import path
from . import views

app_name = 'Accounts'  # Replace with your app's name

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/send-friend-request/', views.send_friend_request, name='send_friend_request'),
    path('friend-requests/', views.friend_requests_view, name='friend_requests'),
    path('respond_to_friend_request/<int:request_id>/<str:action>/', views.respond_to_friend_request, name='respond_to_friend_request'),
    path('block/', views.block, name='block')
]
