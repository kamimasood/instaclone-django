from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Auto-create a Profile based on the user."""
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()