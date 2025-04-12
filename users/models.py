from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model inheriting from AbstractUser.
    We can add custom fields here later if needed.
    For now, it behaves exactly like the default Django User model,
    but provides the flexibility for future customization.
    """
    # Add custom fields here in the future, e.g.:
    # email = models.EmailField(unique=True) # Example: Making email the unique identifier
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # By inheriting AbstractUser, we get fields like:
    # username, first_name, last_name, email, password, groups, user_permissions,
    # is_staff, is_active, is_superuser, last_login, date_joined

    pass # No custom fields added yet

    # You might want to add __str__ method for better representation
    def __str__(self):
        return self.username
