from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('notices/', views.list_notices, name='notices'),
    path('notices/new/', views.create_notice, name='create_notice'),
    path('directory/', views.emergency_directory, name='directory'),
]
