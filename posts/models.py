from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    """Represents an Instagram-like post uploaded by a user."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )

    image = models.ImageField(
        upload_to='posts/images/', blank=True, null=True
        )
    video = models.FileField(
        upload_to='posts/videos/', blank=True, null=True
        )  
    caption = models.TextField(max_length=2200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        """Return a short preview of the caption or the post id."""
        return f'{self.caption[:50]}...' if self.caption else \
        f'Post {self.id}'
    
    def has_media(self):
        """Check if the post has any media."""
        return bool(self.image or self.video)
    
    @property
    def media_type(self):
        if self.image:
            return 'image'
        if self.video:
            return 'video'
        return None
    
    def is_liked_by(self, user):
        """Check if the post is liked by a specific user."""
        return self.likes.filter(user=user).exists()

    def total_likes(self):
        """Return the number of likes the post has received."""
        return self.likes.count()
    
    def total_comments(self):
        """Return the number of comments the post has received."""
        return self.comments.count()