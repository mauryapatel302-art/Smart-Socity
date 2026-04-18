from django.db import models
from core.models import Flat
from django.utils import timezone

class VisitorLog(models.Model):
    VISITOR_TYPES = [
        ('GUEST', 'Guest'),
        ('DELIVERY', 'Delivery'),
        ('MAINTENANCE', 'Maintenance Staff'),
    ]
    name = models.CharField(max_length=100)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='visitors')
    purpose = models.CharField(max_length=200)
    visitor_type = models.CharField(max_length=20, choices=VISITOR_TYPES, default='GUEST')
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} visiting {self.flat}"

class GatePassRequest(models.Model):
    PASS_TYPES = [
        ('TEMPORARY', 'Temporary (Today Only)'),
        ('PERMANENT', 'Permanent (Until Cancelled)'),
    ]
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='gate_passes')
    visitor_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, help_text="Visitor's contact number")
    purpose = models.CharField(max_length=200, blank=True, help_text="e.g. Family, Maid, Delivery")
    pass_type = models.CharField(max_length=20, choices=PASS_TYPES, default='TEMPORARY')
    expected_date = models.DateField(null=True, blank=True, help_text="Required for temporary passes")
    is_approved = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, help_text="Permanent passes are active until resident cancels")
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid_today(self):
        """Returns True if the pass is valid for entry today."""
        from datetime import date
        if self.pass_type == 'PERMANENT':
            return self.is_active
        # TEMPORARY: valid only if expected_date matches today
        return self.expected_date == date.today() and self.is_approved

    def __str__(self):
        return f"[{self.pass_type}] Gate Pass for {self.visitor_name} to {self.flat}"
