from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from interactions.models import Like, Comment
from notifications.models import Notification
from accounts.models import Follow

@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    """The like notification."""

    if created and instance.post.author != instance.user:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            notification_type='like',
            post=instance.post
        )

@receiver(post_delete, sender=Like)
def unlike_remove_notification(sender, instance, **kwargs):
    """Unlike and remove notification."""
    Notification.objects.filter(
        recipient=instance.post.author,
        actor=instance.user,
        notification_type='like',
        post=instance.post
    ).delete()

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    """Comment notification."""
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            notification_type='comment',
            post=instance.post
        )

@receiver(post_save, sender=Follow)
def follow_notification(sender, instance, created, **kwargs):
    """Follow notification."""
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            recipient=instance.following,
            actor=instance.follower,
            notification_type='follow',
            post=instance.post
        )