from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def is_admin_role(self):
        return self.role == 'admin'

    def is_staff_role(self):
        return self.role in ('admin', 'staff')
