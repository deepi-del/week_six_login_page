from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# Admin Profile Model
class AdminProfile(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)  # Use string reference here
    department = models.CharField(max_length=100, blank=True, null=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
