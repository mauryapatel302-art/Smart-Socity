from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.list_complaints, name='list'),
    path('new/', views.create_complaint, name='create'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
]
