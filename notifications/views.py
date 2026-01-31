from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notifications.models import Notification


@login_required
def notifications_list(request):
    """Show the notifications list to the user."""
    notifications = Notification.objects.filter(
        recipient=request.user 
    )

    notifications.filter(is_read=False).update(is_read=True)
    context = {'notifications': notifications}

    return render(request,
                  'notifications/notifications_list.html',
                  context)