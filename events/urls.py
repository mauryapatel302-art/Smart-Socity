from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.list_events, name='events_list'),
    path('new/', views.create_event, name='create_event'),
    path('<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    
    path('polls/', views.list_polls, name='polls_list'),
    path('polls/new/', views.create_poll, name='create_poll'),
    path('polls/<int:poll_id>/vote/', views.vote_poll, name='vote_poll'),
]
