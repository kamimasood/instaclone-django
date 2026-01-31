from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from posts.forms import PostForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def create_post(request):
    """Allow a logged-in user to create a post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)

def post_detail(request, post_id):
    """Display a single post."""
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'posts/post_detail.html', context)

@login_required
def delete_post(request, post_id):
    """Allow a user to delete only their own post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('feed')
    
    context = {'post': post}
    return render(request, 'posts/delete_post.html', context)

def feed(request):
    """Display all posts in reverse chronological order."""
    user = request.user

    posts = Post.objects.select_related('author').order_by('-created_at')

    if user.is_authenticated:
        # Posts from followed users + user's own posts
        followed_ids = user.following.values_list('following_id', 
                                                  flat=True)
        posts = Post.objects.filter(
            author_id__in=list(followed_ids) + [user.id]
            ).select_related('author').order_by('-created_at')

    context = {'posts': posts}
    return render(request, 'posts/feed.html', context)