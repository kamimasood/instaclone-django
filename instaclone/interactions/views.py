from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from interactions.models import Like, Comment

@login_required
def toggle_like(request, post_id):
    """Toggle like or unlike on a post."""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        user=request.user, post=post)
    if not created:  # If it is already liked
        like.delete()
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text.strip():
            Comment.objects.create(user=request.user, post=post)
    return redirect('post_detail', post_id=post.id)
