from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Role
from .forms import SecretarySignUpForm, ResidentSignUpForm, GuardSignUpForm

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        role = request.POST.get('role', '').upper()
        
        if role == 'SECRETARY':
            expected_role = Role.SECRETARY
            role_title = 'Secretary'
        elif role == 'RESIDENT':
            expected_role = Role.RESIDENT
            role_title = 'Resident'
        elif role in ['GUARD', 'SECURITY']:
            expected_role = Role.SECURITY
            role_title = 'Security Guard'
        else:
            messages.error(request, "Invalid role selection.")
            return redirect('landing')
            
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.role != expected_role and not user.is_superuser:
                    messages.error(request, f"Access denied. You are not registered as a {role_title}.")
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/universal_login.html')

def role_signup(request, role_param):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    role = role_param.upper()
    if role == 'SECRETARY':
        form_class = SecretarySignUpForm
        role_title = 'Secretary'
    elif role == 'RESIDENT':
        form_class = ResidentSignUpForm
        role_title = 'Resident'
    elif role == 'GUARD' or role == 'SECURITY':
        form_class = GuardSignUpForm
        role_title = 'Security Guard'
    else:
        messages.error(request, "Invalid role selection.")
        return redirect('landing')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = form_class()

    return render(request, 'accounts/modern_signup.html', {
        'form': form,
        'role_title': role_title,
        'role_param': role_param
    })

def role_login(request, role_param):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    role = role_param.upper()
    if role == 'SECRETARY':
        role_title = 'Secretary'
        expected_role = Role.SECRETARY
    elif role == 'RESIDENT':
        role_title = 'Resident'
        expected_role = Role.RESIDENT
    elif role == 'GUARD' or role == 'SECURITY':
        role_title = 'Security Guard'
        expected_role = Role.SECURITY
    else:
        messages.error(request, "Invalid role selection.")
        return redirect('landing')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.role != expected_role and not user.is_superuser:
                    messages.error(request, f"Access denied. You are not registered as a {role_title}.")
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/role_login.html', {
        'form': form,
        'role_title': role_title,
        'role_param': role_param
    })

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard(request):
    user = request.user
    
    if user.is_secretary():
        from core.models import Flat
        from billing.models import MaintenanceBill
        from complaints.models import Complaint
        from visitors.models import VisitorLog, GatePassRequest
        from django.contrib.auth import get_user_model
        from django.utils import timezone

        User = get_user_model()
        today = timezone.now().date()

        total_residents = User.objects.filter(role='RESIDENT').count()
        total_flats = Flat.objects.count()
        pending_complaints = Complaint.objects.filter(status='OPEN').count()
        today_visitors = VisitorLog.objects.filter(entry_time__date=today).count()

        paid_bills = MaintenanceBill.objects.filter(is_paid=True).count()
        unpaid_bills = MaintenanceBill.objects.filter(is_paid=False).count()
        recent_complaints = Complaint.objects.select_related('resident').order_by('-created_at')[:10]

        today_temp_passes = GatePassRequest.objects.filter(
            expected_date=today, is_approved=True, pass_type='TEMPORARY'
        ).select_related('flat', 'flat__wing')
        permanent_passes = GatePassRequest.objects.filter(
            is_active=True, pass_type='PERMANENT'
        ).select_related('flat', 'flat__wing')

        from collections import defaultdict
        perm_by_flat = defaultdict(lambda: {'flat': None, 'resident': None, 'passes': []})
        for p in permanent_passes:
            key = p.flat.id
            perm_by_flat[key]['flat'] = p.flat
            perm_by_flat[key]['passes'].append(p)
            if not perm_by_flat[key]['resident']:
                resident = User.objects.filter(flat=p.flat, role='RESIDENT').first()
                perm_by_flat[key]['resident'] = resident

        context = {
            'total_residents': total_residents,
            'total_flats': total_flats,
            'pending_complaints': pending_complaints,
            'today_visitors': today_visitors,
            'paid_bills': paid_bills,
            'unpaid_bills': unpaid_bills,
            'recent_complaints': recent_complaints,
            'today_temp_passes': today_temp_passes,
            'perm_by_flat': list(perm_by_flat.values()),
            'temp_pass_count': today_temp_passes.count(),
            'perm_pass_count': permanent_passes.count(),
        }
        return render(request, 'accounts/dashboard_secretary.html', context)
        
    elif user.is_resident():
        from billing.models import MaintenanceBill
        from complaints.models import Complaint
        from core.models import Notice
        from events.models import Event
        from django.utils import timezone

        today = timezone.now().date()

        my_unpaid_bills = MaintenanceBill.objects.filter(flat=user.flat, is_paid=False) if user.flat else []
        my_paid_bills_count = MaintenanceBill.objects.filter(flat=user.flat, is_paid=True).count() if user.flat else 0
        my_unpaid_bills_count = len(my_unpaid_bills)

        my_open_complaints = Complaint.objects.filter(resident=user, status__in=['OPEN', 'IN_PROGRESS'])
        my_all_complaints = Complaint.objects.filter(resident=user).order_by('-created_at')[:5]

        recent_notices = Notice.objects.all().order_by('-created_at')[:4]
        upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:3]

        context = {
            'my_unpaid_bills': my_unpaid_bills,
            'my_paid_bills_count': my_paid_bills_count,
            'my_unpaid_bills_count': my_unpaid_bills_count,
            'my_open_complaints': my_open_complaints,
            'my_all_complaints': my_all_complaints,
            'recent_notices': recent_notices,
            'upcoming_events': upcoming_events,
        }
        return render(request, 'accounts/dashboard_resident.html', context)
    
    else:
        from visitors.models import VisitorLog, GatePassRequest
        from django.utils import timezone
        from collections import defaultdict

        today = timezone.now().date()

        active_visitors = VisitorLog.objects.filter(exit_time__isnull=True).order_by('-entry_time')
        all_visitors_today = VisitorLog.objects.filter(entry_time__date=today).order_by('-entry_time')

        today_temp_passes = GatePassRequest.objects.filter(
            expected_date=today, is_approved=True, pass_type='TEMPORARY'
        ).select_related('flat', 'flat__wing')

        permanent_passes = GatePassRequest.objects.filter(
            is_active=True, pass_type='PERMANENT'
        ).select_related('flat', 'flat__wing')

        # Group permanent passes by flat, with resident info
        from django.contrib.auth import get_user_model
        User = get_user_model()

        perm_by_flat = defaultdict(lambda: {'flat': None, 'resident': None, 'passes': []})
        for p in permanent_passes:
            key = p.flat.id
            perm_by_flat[key]['flat'] = p.flat
            perm_by_flat[key]['passes'].append(p)
            if not perm_by_flat[key]['resident']:
                resident = User.objects.filter(flat=p.flat, role='RESIDENT').first()
                perm_by_flat[key]['resident'] = resident

        return render(request, 'accounts/dashboard_security.html', {
            'active_visitors': active_visitors,
            'all_visitors_today': all_visitors_today,
            'today_temp_passes': today_temp_passes,
            'perm_by_flat': list(perm_by_flat.values()),
            'active_count': active_visitors.count(),
            'total_today': all_visitors_today.count(),
            'temp_pass_count': today_temp_passes.count(),
            'perm_pass_count': permanent_passes.count(),
        })

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    from .forms import UserUpdateForm
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
        
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def resident_list(request):
    user = request.user
    if not hasattr(user, 'is_secretary') or not user.is_secretary():
        messages.error(request, "Access denied. Only secretaries can view this page.")
        return redirect('dashboard')
        
    from .models import CustomUser
    residents = CustomUser.objects.filter(role='RESIDENT').select_related('flat', 'flat__wing').order_by('flat__wing__name', 'flat__number', 'first_name')
    return render(request, 'accounts/resident_list.html', {'residents': residents})
