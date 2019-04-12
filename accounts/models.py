import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Pharmacy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=9)

    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

