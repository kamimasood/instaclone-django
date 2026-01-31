from django.db import models
from django.conf import settings
from django.utils import timezone
from posts.models import Post

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """Instagram-style notification model."""
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES
    )

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        null=True, blank=True
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the app."""
        return f'{self.actor} -> {self.recipient} ({self.notification_type})'