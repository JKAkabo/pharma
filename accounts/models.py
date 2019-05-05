import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_full_name()

