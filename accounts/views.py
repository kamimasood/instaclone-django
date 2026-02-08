from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Profile, User, Follow
from accounts.forms import SignUpForm, LoginForm, UserEditForm, ProfileEditForm
from posts.models import Post

def home(request):
    """Redirect logged users to feed."""
    if request.user.is_authenticated:
        return redirect('posts:feed')
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

    if request.user.is_authenticated and not is_own_profile:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    # User posts
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'posts': posts,
        'followers': user.followers_count(),
        'following': user.following_count(),
        'post_count': posts.count(),
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def followers_list(request, username):
    """View for viewing followers list of a user."""
    user = get_object_or_404(User, username=username)
    followers = User.objects.filter(
        following__following=user
    ).select_related('profile')

    context = {'title': 'Followers', 'users': followers}
    return render(request, 'accounts/follow_list.html', context)

@login_required
def following_list(request, username):
    """View for viewing following list of a user."""
    user = get_object_or_404(User, username=username)
    following = User.objects.filter(
        followers__follower=user
    ).select_related('profile')

    context = {'title': 'Following', 'users': following}
    return render(request, 'accounts/follow_list.html', context)

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

def search_accounts(request):
    """Implement the search bar view."""
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(profile__full_name__icontains=query)
        ).select_related('profile')
    
    context = {'query': query, 'users': users}
    return render(request, 'accounts/search_results.html', context)

@login_required
def search_accounts_ajax(request):
    """Implement the search accounts functionality."""
    query = request.GET.get('q', '').strip()

    results = []

    if query:
        users = (
            User.objects
            .filter(
                Q(username__icontains=query) | 
                Q(profile__full_name__icontains=query)
            )
            .select_related('profile')[:8]
        )

        for user in users:
            results.append({
                'username': user.username,
                'profile_url': user.get_absolute_url(),
                'avatar': user.profile.avatar.url if user.profile.avatar else '/static/img/default-avatar.png',
                'display_name': user.profile.get_display_name(),
            })
    '''
    html = render_to_string(
        'accounts/search_results.html',
        {'users': users},
        request
    )
    '''
    return JsonResponse({'results': results})
    
@login_required
def edit_profile(request):
    """View for editing user's own profile."""
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('profile', username=user.username)
    else:
        form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)
    
    context = {
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit_profile.html', context)