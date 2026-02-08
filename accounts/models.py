from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

class User(AbstractUser):
    """A custom user nodel extending Django's AbstractUser."""
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,
                                    blank=True, null=True)
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        """Return the username as the string representation."""
        return self.username
    
    def followers_count(self):
        """Return the number of followers the user has."""
        return self.followers.count()

    def following_count(self):
        """Return the number of following the user has."""
        return self.following.count()
    
    def posts_count(self):
        """
        Return the number of posts the user has.
        Work if Post model has User as a foreign key.
        """
        return self.posts.count()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})

class Profile(models.Model):
    """A profile model extending the User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    full_name = models.CharField(max_length=200, 
                                 blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d',  # Improved upload path 
                               default='avatars/default.png')
    location = models.CharField(max_length=100, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        """Return the username for readability.""" 
        return f'{self.user.username}\'s profile'

    def get_display_name(self):
        """Return full name if available, otherwise username."""
        return self.full_name.title() if self.full_name else \
        self.user.username 

class Follow(models.Model):
    """Represent 'who follows who'."""

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
        )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
        )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        """Readable string showing follow relationship."""
        return f'{self.follower.username}' + \
            f'follows {self.following.username}'
    
    def is_mutual(self):
        """Return True if the following user also follows back."""
        return Follow.objects.filter(
            follower=self.following, following=self.follower
            ).exists()