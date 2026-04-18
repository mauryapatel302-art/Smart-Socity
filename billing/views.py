from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MaintenanceBill, Payment
from core.models import Flat
import uuid
import datetime

@login_required
def generate_bills(request):
    user = request.user
    if not hasattr(user, 'is_secretary') or not user.is_secretary():
        messages.error(request, "Access denied. Only secretaries can generate bills.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')
        
        if not all([month, year, amount, due_date]):
            messages.error(request, "All fields are required to generate a bill.")
            return redirect('generate_bills')
            
        try:
            amt_val = float(amount)
            if amt_val <= 0:
                messages.error(request, "Bill amount must be greater than zero.")
                return redirect('generate_bills')
        except ValueError:
            messages.error(request, "Invalid amount format.")
            return redirect('generate_bills')
            
        flats = Flat.objects.all()
        created_count = 0
        
        for flat in flats:
            bill, created = MaintenanceBill.objects.get_or_create(
                flat=flat,
                month=month,
                year=year,
                defaults={
                    'amount': amount,
                    'due_date': due_date
                }
            )
            if created:
                created_count += 1
                
        messages.success(request, f"Successfully generated {created_count} bills for {month} {year}.")
        return redirect('dashboard')
        
    return render(request, 'billing/generate_bills.html')

@login_required
def my_bills(request):
    user = request.user
    if not hasattr(user, 'is_resident') or not user.is_resident() or not user.flat:
        messages.error(request, "You need a flat assignment to view bills.")
        return redirect('dashboard')
        
    bills = MaintenanceBill.objects.filter(flat=user.flat).order_by('-year', '-month')
    return render(request, 'billing/my_bills.html', {'bills': bills})

@login_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, id=bill_id, flat=request.user.flat)
    
    if bill.is_paid:
        messages.info(request, "This bill is already paid.")
        return redirect('my_bills')
        
    if request.method == 'POST':
        method = request.POST.get('method', 'UPI')
        
        payment = Payment.objects.create(
            bill=bill,
            method=method,
            transaction_id=str(uuid.uuid4()).split('-')[0].upper()
        )
        bill.is_paid = True
        bill.save()
        
        messages.success(request, f"Payment successful! Transaction ID: {payment.transaction_id}")
        return redirect('my_bills')
        
    return render(request, 'billing/pay_bill.html', {'bill': bill})

@login_required
def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, bill__flat=request.user.flat)
    return render(request, 'billing/receipt.html', {'payment': payment})

@login_required
def billing_status(request):
    user = request.user
    if not hasattr(user, 'is_secretary') or not user.is_secretary():
        messages.error(request, "Access denied. Only secretaries can view this page.")
        return redirect('dashboard')
        
    bills = MaintenanceBill.objects.all().select_related('flat', 'flat__wing').order_by('-year', '-month', 'flat__wing__name', 'flat__number')
    return render(request, 'billing/status.html', {'bills': bills})
