from django.db import models
from apps.master.models import BaseModel
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
# Create your models here.

def profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"user_{instance.id}.{ext}"
    return os.path.join("profile_pics", filename)

class User(BaseModel):
    profile = models.ImageField(
        upload_to=profile_upload_path,
        default="profile_pics/default.png",
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    mobile = models.CharField(max_length=255, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, default="875354")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=255, blank=True, null=True)
    line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)

class Inqueries(BaseModel):
    STATUS_CHOISES = [
        ("Pending", "Pending"),
        ("Resolved", "Resolved")
    ]
    fullname = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    message = models.TextField()
    status = models.CharField(default="Pending", choices=STATUS_CHOISES)

@receiver(pre_save, sender=User)
def delete_old_profile(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_profile = User.objects.get(pk=instance.pk).profile
    except User.DoesNotExist:
        return

    new_profile = instance.profile

    if old_profile and old_profile != new_profile:
        if old_profile.name != "profile_pics/default.png":
            if os.path.isfile(old_profile.path):
                os.remove(old_profile.path)

@receiver(post_delete, sender=User)
def delete_profile_on_delete(sender, instance, **kwargs):
    if instance.profile:
        if instance.profile.name != "profile_pics/default.png":
            if os.path.isfile(instance.profile.path):
                os.remove(instance.profile.path)
