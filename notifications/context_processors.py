from chats.models import Message

def unread_counts(request):
    """Use a context processor."""

    unread_notifications = 0
    unread_messages= 0

    if request.user.is_authenticated:
        # Unread like/comment/follow
        unread_notifications = request.user.notifications.filter(
            is_read = False
        ).count()

        # Unread messages
        unread_messages = Message.objects.filter(
            reciever = request.user,
            is_read = False
        ).count()

    context = {
        'unread_notifications': unread_notifications,
        'unread_messages': unread_messages
    }
    return context