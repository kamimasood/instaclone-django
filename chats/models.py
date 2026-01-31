from django.db import models
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL

class Message(models.Model):
    """A simple model representing user's messages."""

    sender = models.ForeignKey(
        User, related_name='sent_messages',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User, related_name='received_messages',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the model."""
        return f'{self.sender} -> '