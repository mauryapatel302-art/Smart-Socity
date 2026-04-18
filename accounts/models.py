from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    SECRETARY = 'SECRETARY', 'Secretary'
    RESIDENT = 'RESIDENT', 'Resident'
    SECURITY = 'SECURITY', 'Security'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.RESIDENT)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_on_duty = models.BooleanField(default=False, help_text="Designates whether this staff member is currently working.")
    
    # We will relate this to the Flat model in the core app.
    # To avoid circular imports initially, we can use a string reference 'core.Flat'.
    flat = models.ForeignKey('core.Flat', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')

    def is_secretary(self):
        return self.role == Role.SECRETARY

    def is_resident(self):
        return self.role == Role.RESIDENT
        
    def is_security(self):
        return self.role == Role.SECURITY

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
