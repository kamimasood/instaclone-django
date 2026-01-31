from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from chats.models import Message

User = get_user_model()

@login_required
def inbox(request):
    """The inbox view."""
    messages = Message.objects.filter(
        receiver=request.user,
    ).select_related('sender').order_by('-created_at')

    context = {'messages': messages}
    return render(request, 'chats/inbox.html', context)

@login_required
def start_chat(request, username):
    """Validate the user and redirect to conversation."""
    other_user = get_object_or_404(User, username=username)

    # Prevent chatting with yourself.
    if other_user == request.user:
        return redirect('profile', username=request.user.username)
    
    return redirect('chats:conversation', username=other_user.username)

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user],
    ).order_by('created_at')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )
            return redirect('chats:conversation', username=other_user)
        
    context = {
        'messages': messages,
        'other_user': other_user
        }
    return render(request, 'chats/conversation.html', context)