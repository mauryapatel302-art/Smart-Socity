from django.db import models
from core.models import Flat

class MaintenanceBill(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='bills')
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    late_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('flat', 'month', 'year')
        
    def __str__(self):
        return f"Bill for {self.flat} - {self.month} {self.year}"

class Payment(models.Model):
    bill = models.OneToOneField(MaintenanceBill, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[('UPI', 'UPI'), ('CARD', 'Card'), ('CASH', 'Cash')])
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"Payment for {self.bill}"
