import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from pharma.settings.base import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver




class Pharmacy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gps_location = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=9)

    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE)

    #profile_pic = models.ImageField(upload_to='upload/', blank=True)

    def __str__(self):
        return self.get_full_name()

class UserImage(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE )
    profile_pic = models.ImageField(upload_to='upload/', blank=True)

# @receiver(post_save, sender=AUTH_USER_MODEL)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserImage.objects.create(user=instance)

# @receiver(post_save, sender=AUTH_USER_MODEL)
# def save_profile(sender, instance, **kwargs):
#     instance.profile_pic.save()        
