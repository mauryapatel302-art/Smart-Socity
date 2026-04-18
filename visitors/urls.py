from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('security/', views.security_dashboard, name='security_dashboard'),
    path('security/new/', views.create_visitor, name='create_visitor'),
    path('security/<int:visitor_id>/checkout/', views.checkout_visitor, name='checkout_visitor'),
    
    path('passes/', views.my_gate_passes, name='my_gate_passes'),
    path('passes/new/', views.create_gate_pass, name='create_gate_pass'),
    path('passes/<int:pass_id>/cancel/', views.cancel_permanent_pass, name='cancel_permanent_pass'),
]
