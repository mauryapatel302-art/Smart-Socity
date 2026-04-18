from django.db import models
from django.conf import settings

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('PLUMBING', 'Plumbing'),
        ('ELECTRICITY', 'Electricity'),
        ('PARKING', 'Parking'),
        ('NOISE', 'Noise'),
        ('OTHER', 'Other'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    photo = models.ImageField(upload_to='complaints/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
