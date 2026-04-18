from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_bills, name='generate_bills'),
    path('my-bills/', views.my_bills, name='my_bills'),
    path('pay/<int:bill_id>/', views.pay_bill, name='pay_bill'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
    path('status/', views.billing_status, name='billing_status'),
]
