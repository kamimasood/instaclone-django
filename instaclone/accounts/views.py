from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, User, Follow
from accounts.forms import SignUpForm, LoginForm


def home(request):
    """Redirect logged users to feed."""
    return render(request, 'accounts/home.html')

def signup(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('posts:feed')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,
                                password=password)
            if user:
                login(request, user)
                return redirect('posts:feed')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

@login_required
def profile_view(request, username):
    """Display a user's profile page."""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    is_own_profile = request.user == user
    is_following = False

    if request.user.is_authenticated and is_own_profile:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    context = {
        'user': user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'followers': user.followers_count(),
        'followings': user.following_count(),
        'posts': user.posts_count(),
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def toggle_follow(request, username):
    """
    Toggle follow and unfollow between the current user
    and another user.
    Later: 
        - Enforce privacy
        - Create follow request model for private accounts 
    """
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('profile', username=username)
    
    existing = Follow.objects.filter(
        follower=request.user, following=target_user
    )

    if existing.exists():
        # Unfollow
        existing.delete()
    else:
        # Follow
        Follow.objects.create(follower=request.user,
                              following=target_user)
    
    return redirect('profile', username=username)