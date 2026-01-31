from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from posts.models import Post
from interactions.models import Like, Comment

@login_required
@require_POST
def toggle_like(request, post_id):
    """Toggle like or unlike on a post."""
    post = get_object_or_404(Post, id=post_id)


    like = Like.objects.get_or_create(
        user=request.user, 
        post=post
    )

    if not created:
        like.delete()
        liked = False
    else:
        return


    # return redirect(request.META.get())
    return JsonResponse(
        {
            'liked': liked,
            'likes_count': post.likes.count()
        }
    )

@login_required
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(Post, id=post_id)

    text = request.POST.get('text')
    if text and text.strip():
        Comment.objects.create(
            user=request.user, 
            post=post,
            text=text.strip())
    
    return redirect(request.META.get('HTTP_REFERER'))