from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('<str:username>/followers/', views.followers_list, name='followers'),
    path('<str:username>/following/', views.following_list, name='following'),
    path('search/', views.search_accounts, name='search'),
    path('search/ajax/', views.search_accounts_ajax, name='search_ajax'),
    path('edit/', views.edit_profile, name='edit_profile'),
]