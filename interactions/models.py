from django.db import models
from django.utils import timezone
from django.conf import settings
from posts.models import Post

User = settings.AUTH_USER_MODEL

class Like(models.Model):
    """Represents a 'like' given by a user to a post."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        """Readable string representation of a like."""
        return f'{self.user} liked Post {self.post_id}'

class Comment(models.Model):
    """Represents a comment made by a user on a post."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Short preview of the comment."""
        return f'{self.user.username}: {self.text[:30]}...'