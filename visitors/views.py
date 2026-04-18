from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import VisitorLog, GatePassRequest
from core.models import Flat
from datetime import date

@login_required
def security_dashboard(request):
    if not hasattr(request.user, 'is_security') or not request.user.is_security():
        return redirect('dashboard')

    today = date.today()

    active_visitors = VisitorLog.objects.filter(exit_time__isnull=True).order_by('-entry_time')
    all_visitors_today = VisitorLog.objects.filter(entry_time__date=today).order_by('-entry_time')

    today_temp_passes = GatePassRequest.objects.filter(
        expected_date=today, is_approved=True, pass_type='TEMPORARY'
    ).select_related('flat')
    permanent_passes = GatePassRequest.objects.filter(
        is_active=True, pass_type='PERMANENT'
    ).select_related('flat')

    return render(request, 'visitors/security_log.html', {
        'active_visitors': active_visitors,
        'today_passes': today_temp_passes,
        'permanent_passes': permanent_passes,
    })

@login_required
def create_visitor(request):
    if not hasattr(request.user, 'is_security') or not request.user.is_security():
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name', '')
        flat_id = request.POST.get('flat')
        visitor_type = request.POST.get('visitor_type', '')
        purpose = request.POST.get('purpose', '')
        
        if not name.strip() or not flat_id or not visitor_type.strip():
            messages.error(request, "Visitor Name, Flat, and Visitor Type are strictly required.")
            return redirect('visitors:create_visitor')
            
        flat = get_object_or_404(Flat, id=flat_id)
        VisitorLog.objects.create(name=name, flat=flat, visitor_type=visitor_type, purpose=purpose)
        messages.success(request, f"Entry logged for {name} visiting {flat}.")
        return redirect('visitors:security_dashboard')
        
    return render(request, 'visitors/create_visitor.html', {
        'flats': Flat.objects.all(),
        'visitor_types': VisitorLog.VISITOR_TYPES
    })

@login_required
def checkout_visitor(request, visitor_id):
    if not hasattr(request.user, 'is_security') or not request.user.is_security():
        return redirect('dashboard')
        
    visitor = get_object_or_404(VisitorLog, id=visitor_id, exit_time__isnull=True)
    visitor.exit_time = timezone.now()
    visitor.save()
    messages.success(request, f"{visitor.name} checked out successfully.")
    return redirect('visitors:security_dashboard')

@login_required
def my_gate_passes(request):
    if not hasattr(request.user, 'is_resident') or not request.user.is_resident() or not request.user.flat:
        messages.error(request, "You need a flat assignment to use Gate Passes.")
        return redirect('dashboard')
        
    temp_passes = GatePassRequest.objects.filter(
        flat=request.user.flat, pass_type='TEMPORARY'
    ).order_by('-expected_date')
    
    permanent_passes = GatePassRequest.objects.filter(
        flat=request.user.flat, pass_type='PERMANENT'
    ).order_by('-created_at')
    
    return render(request, 'visitors/my_passes.html', {
        'temp_passes': temp_passes,
        'permanent_passes': permanent_passes,
    })

@login_required
def create_gate_pass(request):
    if not hasattr(request.user, 'is_resident') or not request.user.is_resident() or not request.user.flat:
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('visitor_name')
        phone = request.POST.get('phone', '')
        purpose = request.POST.get('purpose', '')
        pass_type = request.POST.get('pass_type', 'TEMPORARY')
        expected_date = request.POST.get('expected_date') or None

        if pass_type == 'TEMPORARY':
            if not expected_date:
                messages.error(request, "Please select a valid date for a Temporary Gate Pass.")
                return redirect('visitors:create_gate_pass')
            from datetime import datetime
            try:
                if datetime.strptime(expected_date, '%Y-%m-%d').date() < date.today():
                    messages.error(request, "Gate pass request cannot be made for a past date.")
                    return redirect('visitors:create_gate_pass')
            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect('visitors:create_gate_pass')
        
        GatePassRequest.objects.create(
            flat=request.user.flat,
            visitor_name=name,
            phone=phone,
            purpose=purpose,
            pass_type=pass_type,
            expected_date=expected_date if pass_type == 'TEMPORARY' else None,
            is_active=True,
        )
        label = "Temporary" if pass_type == 'TEMPORARY' else "Permanent"
        messages.success(request, f"{label} Gate Pass created for {name}.")
        return redirect('visitors:my_gate_passes')
        
    return render(request, 'visitors/create_pass.html', {
        'today': date.today().strftime('%Y-%m-%d'),
    })

@login_required
def cancel_permanent_pass(request, pass_id):
    if not hasattr(request.user, 'is_resident') or not request.user.is_resident():
        return redirect('dashboard')

    gate_pass = get_object_or_404(GatePassRequest, id=pass_id, flat=request.user.flat, pass_type='PERMANENT')
    gate_pass.is_active = False
    gate_pass.save()
    messages.success(request, f"Permanent pass for {gate_pass.visitor_name} has been cancelled.")
    return redirect('visitors:my_gate_passes')
