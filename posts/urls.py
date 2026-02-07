from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('new/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
]