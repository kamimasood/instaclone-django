from django.urls import path
from chats import views

app_name = 'chats'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<str:username>/', views.conversation, name='conversation'),
    path('start/<str:username>/', views.start_chat, name='start_chat'),
]