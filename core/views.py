from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice
from django.utils import timezone

@login_required
def list_notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'core/notices.html', {'notices': notices})

@login_required
def create_notice(request):
    if not hasattr(request.user, 'is_secretary') or not request.user.is_secretary():
        messages.error(request, "Only secretaries can post notices.")
        return redirect('core:notices')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        attachment = request.FILES.get('attachment')
        start_date = request.POST.get('start_date')
        expiry_date = request.POST.get('expiry_date')
        
        Notice.objects.create(
            title=title,
            description=description,
            category=category,
            attachment=attachment,
            start_date=start_date,
            expiry_date=expiry_date,
            created_by=request.user
        )
        messages.success(request, "Notice posted successfully!")
        return redirect('core:notices')
        
    return render(request, 'core/create_notice.html', {'categories': Notice.CATEGORY_CHOICES})

@login_required
def emergency_directory(request):
    from .models import EmergencyContact
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    db_contacts = list(EmergencyContact.objects.all().order_by('name'))
    
    # Append the staff contacts dynamically
    # Pick 1 Secretary
    sec = User.objects.filter(role='SECRETARY').first()
    # Pick max 2 guards on duty
    guards = User.objects.filter(role='SECURITY', is_on_duty=True)[:2]
    
    staff_contacts = []
    
    # Process Secretary
    if sec:
        staff_contacts.append({
            'name': sec.get_full_name() or sec.username,
            'role_or_category': 'Secretary',
            'phone': sec.phone or "Not provided",
            'photo_url': sec.profile_photo.url if sec.profile_photo else None
        })
        
    # Process Guards
    for guard in guards:
        staff_contacts.append({
            'name': guard.get_full_name() or guard.username,
            'role_or_category': 'Security Guard (On Duty)',
            'phone': guard.phone or "Not provided",
            'photo_url': guard.profile_photo.url if guard.profile_photo else None
        })
        
    all_contacts = db_contacts + staff_contacts
    residents = User.objects.filter(role='RESIDENT').order_by('first_name')
    
    return render(request, 'core/directory.html', {
        'contacts': all_contacts,
        'residents': residents
    })

