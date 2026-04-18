from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint

@login_required
def list_complaints(request):
    user = request.user
    if hasattr(user, 'is_secretary') and user.is_secretary():
        complaints = Complaint.objects.all().order_by('-created_at')
    else:
        complaints = Complaint.objects.filter(resident=user).order_by('-created_at')
    
    return render(request, 'complaints/list.html', {'complaints': complaints})

@login_required
def create_complaint(request):
    user = request.user
    if not hasattr(user, 'is_resident') or not user.is_resident():
        messages.error(request, "Only residents can file complaints.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        category = request.POST.get('category')
        photo = request.FILES.get('photo')
        
        if not title.strip() or not description.strip():
            messages.error(request, "Complaint title and description cannot be empty.")
            return redirect('complaints:create')
            
        Complaint.objects.create(
            resident=user,
            title=title,
            description=description,
            category=category,
            photo=photo
        )
        messages.success(request, "Your complaint has been logged successfully.")
        return redirect('complaints:list')
        
    return render(request, 'complaints/create.html', {'categories': Complaint.CATEGORY_CHOICES})

@login_required
def update_status(request, pk):
    user = request.user
    if not hasattr(user, 'is_secretary') or not user.is_secretary():
        messages.error(request, "Only secretaries can update complaints.")
        return redirect('dashboard')
        
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.save()
            messages.success(request, f"Complaint '{complaint.title}' status updated to {complaint.get_status_display()}.")
    return redirect('complaints:list')
