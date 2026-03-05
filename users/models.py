from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save       # ✅ Needed for signals
from django.dispatch import receiver                  # ✅ Needed for @receiver decorator
# Extend Django User with Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    preferred_language = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()