from django.contrib import admin
from .models import Event, EventRSVP, Poll, PollOption, PollVote

admin.site.register(Event)
admin.site.register(EventRSVP)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)
