from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    storage_used = models.BigIntegerField(default=0, help_text="Storage used in bytes.")

    def __str__(self):
        return self.username
