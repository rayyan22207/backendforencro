from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('chats/<str:room_name>/',views.chat, name='chats'),
    path('direct/<str:username>/', views.otochat, name='otochat'),
    path('direct/call/<str:username>/', views.otocall, name='otochat'),
]