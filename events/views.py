from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRSVP, Poll, PollOption, PollVote
from django.utils import timezone
from datetime import date

@login_required
def list_events(request):
    events = Event.objects.filter(date__gte=date.today()).order_by('date')
    
    user_rsvp_ids = []
    if hasattr(request.user, 'is_resident') and request.user.is_resident():
        user_rsvp_ids = EventRSVP.objects.filter(resident=request.user).values_list('event_id', flat=True)
        
    return render(request, 'events/events_list.html', {
        'events': events,
        'user_rsvp_ids': list(user_rsvp_ids)
    })

@login_required
def create_event(request):
    if not hasattr(request.user, 'is_secretary') or not request.user.is_secretary():
        messages.error(request, "Only secretaries can create events.")
        return redirect('events:events_list')
        
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        event_date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location', '')
        
        if not title.strip() or not event_date:
            messages.error(request, "Event title and date are required.")
            return redirect('events:create_event')
            
        from datetime import datetime
        try:
            if datetime.strptime(event_date, '%Y-%m-%d').date() < date.today():
                messages.error(request, "An event cannot be scheduled in the past.")
                return redirect('events:create_event')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('events:create_event')
        
        Event.objects.create(
            title=title,
            description=description,
            date=event_date,
            time=time,
            venue=location,
            created_by=request.user
        )
        messages.success(request, "Event created successfully!")
        return redirect('events:events_list')
        
    return render(request, 'events/create_event.html')

@login_required
def rsvp_event(request, event_id):
    if not hasattr(request.user, 'is_resident') or not request.user.is_resident():
        return redirect('events:events_list')
        
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        guests_count = request.POST.get('guests_count', 0)
        
        is_going = (status == 'GOING')
        rsvp, created = EventRSVP.objects.update_or_create(
            event=event,
            resident=request.user,
            defaults={'is_attending': is_going}
        )
        messages.success(request, f"Your RSVP for '{event.title}' has been {'confirmed' if is_going else 'cancelled'}!")
        
    return redirect('events:events_list')

@login_required
def list_polls(request):
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    
    user_voted_poll_ids = []
    if hasattr(request.user, 'is_resident') and request.user.is_resident():
        user_voted_poll_ids = PollVote.objects.filter(resident=request.user).values_list('poll_id', flat=True)
        
    return render(request, 'events/polls_list.html', {
        'polls': polls,
        'user_voted_poll_ids': list(user_voted_poll_ids)
    })

@login_required
def create_poll(request):
    if not hasattr(request.user, 'is_secretary') or not request.user.is_secretary():
        messages.error(request, "Only secretaries can create polls.")
        return redirect('events:polls_list')
        
    if request.method == 'POST':
        question = request.POST.get('question', '')
        options = request.POST.getlist('options')
        
        valid_options = [opt.strip() for opt in options if opt.strip()]
        if not question.strip() or len(valid_options) < 2:
            messages.error(request, "A poll requires a question and at least two valid options.")
            return redirect('events:create_poll')
        
        poll = Poll.objects.create(question=question.strip(), is_active=True)
        for opt in valid_options:
            PollOption.objects.create(poll=poll, option_text=opt)
            
        messages.success(request, "Poll created successfully!")
        return redirect('events:polls_list')
        
    return render(request, 'events/create_poll.html')

@login_required
def vote_poll(request, poll_id):
    if not hasattr(request.user, 'is_resident') or not request.user.is_resident():
        return redirect('events:polls_list')
        
    poll = get_object_or_404(Poll, id=poll_id, is_active=True)
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        if option_id:
            option = get_object_or_404(PollOption, id=option_id, poll=poll)
            if PollVote.objects.filter(poll=poll, resident=request.user).exists():
                messages.error(request, "You have already voted on this poll.")
            else:
                PollVote.objects.create(poll=poll, resident=request.user, option=option)
                messages.success(request, "Your vote has been recorded!")
                
    return redirect('events:polls_list')
