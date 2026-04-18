from django.urls import path
from . import views

urlpatterns = [
    path('login/<str:role_param>/', views.role_login, name='role_login'),
    path('signup/<str:role_param>/', views.role_signup, name='role_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('residents/', views.resident_list, name='resident_list'),
    path('', views.landing_page, name='landing'),
]
