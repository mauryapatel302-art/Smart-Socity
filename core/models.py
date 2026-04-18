from django.db import models

class Wing(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text="e.g., A, B, C")

    def __str__(self):
        return f"Wing {self.name}"

class Flat(models.Model):
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE, related_name="flats")
    number = models.CharField(max_length=10, help_text="e.g., 101, 102")
    
    class Meta:
        unique_together = ('wing', 'number')

    def __str__(self):
        return f"{self.wing.name}-{self.number}"

class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=20, unique=True)
    assigned_to = models.OneToOneField(Flat, on_delete=models.SET_NULL, null=True, blank=True, related_name="parking_slot")

    def __str__(self):
        return self.slot_number

class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('EMERGENCY', 'Emergency'),
        ('GENERAL', 'General'),
        ('EVENT', 'Event'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL')
    attachment = models.FileField(upload_to='notices/', null=True, blank=True)
    start_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, related_name='posted_notices')

    def __str__(self):
        return self.title

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    role_or_category = models.CharField(max_length=100, help_text="e.g., Hospital, Plumber, Secretary")
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.role_or_category}"
