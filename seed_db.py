import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsociety.settings')
django.setup()

from accounts.models import CustomUser
from core.models import Wing, Flat, ParkingSlot, Notice, EmergencyContact
from billing.models import MaintenanceBill, Payment
from complaints.models import Complaint
from events.models import Event, EventRSVP, Poll, PollOption, PollVote
from visitors.models import VisitorLog, GatePassRequest

def seed():
    print("Clearing database...")
    CustomUser.objects.exclude(is_superuser=True).delete()
    Wing.objects.all().delete()
    Notice.objects.all().delete()
    EmergencyContact.objects.all().delete()
    Event.objects.all().delete()
    Poll.objects.all().delete()
    MaintenanceBill.objects.all().delete()
    VisitorLog.objects.all().delete()

    print("Creating core structure...")
    wing_a = Wing.objects.create(name='A')
    wing_b = Wing.objects.create(name='B')
    
    all_flats = []
    for fl_no in range(1, 6):
        for unit in range(1, 5):
            all_flats.append(Flat.objects.create(wing=wing_a, number=f"{fl_no}0{unit}"))
            all_flats.append(Flat.objects.create(wing=wing_b, number=f"{fl_no}0{unit}"))

    print("Creating members...")
    sec, _ = CustomUser.objects.get_or_create(
        username='secretary1', 
        defaults={'email': 'sec@test.com', 'role':'SECRETARY', 'first_name':'Rajesh', 'last_name':'Patel', 'phone': '98765-43210'}
    )
    sec.set_password('password123')
    sec.save()
    
    guard, _ = CustomUser.objects.get_or_create(
        username='guard1', 
        defaults={'email': 'guard@test.com', 'role':'SECURITY', 'first_name':'Ramesh', 'last_name':'Yadav', 'phone': '99887-76655'}
    )
    guard.set_password('password123')
    guard.save()
    
    residents = []
    names = [('Amit','Shah'),('Priya','Mehta'),('Suresh','Nair'),('Deepa','Iyer'),('Rahul','Gupta')]
    for i in range(5):
        flat = all_flats[i]
        user, _ = CustomUser.objects.get_or_create(
            username=f'resident{i+1}',
            defaults={'email': f'resident{i+1}@test.com', 'role':'RESIDENT', 'first_name':names[i][0], 'last_name':names[i][1], 'flat':flat}
        )
        user.set_password('password123')
        user.save()
        residents.append(user)

    print("Creating Notices & Emergencies...")
    Notice.objects.create(
        title="Annual General Meeting",
        description="Dear residents, the AGM is scheduled for Sunday, 10 AM at the clubhouse. Attendance is mandatory.",
        category='GENERAL',
        created_by=sec,
        start_date=timezone.now().date(),
        expiry_date=timezone.now().date() + timedelta(days=7)
    )
    Notice.objects.create(
        title="Water Supply Interruption",
        description="Water supply will be suspended tomorrow from 10 AM to 2 PM for tank cleaning. Please store water accordingly.",
        category='MAINTENANCE',
        created_by=sec,
        start_date=timezone.now().date(),
        expiry_date=timezone.now().date() + timedelta(days=1)
    )
    EmergencyContact.objects.create(
        name="Deepak Electrician",
        role_or_category="Electrician",
        phone="88888-99999"
    )
    EmergencyContact.objects.create(
        name="City Hospital",
        role_or_category="Hospital",
        phone="022-12345678"
    )
    EmergencyContact.objects.create(
        name="Quick Plumber",
        role_or_category="Plumber",
        phone="77777-11111"
    )

    print("Creating sample Bills...")
    for res in residents:
        MaintenanceBill.objects.create(
            flat=res.flat, month='April', year=2026, amount=2500.00,
            due_date=timezone.now().date() + timedelta(days=5)
        )
        
    print("Creating Events...")
    event = Event.objects.create(
        title="Holi Milan",
        description="Join us for a colorful evening at the clubhouse!",
        date=timezone.now().date() + timedelta(days=2),
        time=timezone.now().time(),
        venue="Clubhouse Lawn",
        created_by=sec
    )
    
    EventRSVP.objects.create(event=event, resident=residents[0], is_attending=True)
    
    poll = Poll.objects.create(question="Which day for society cleanup?", is_active=True)
    PollOption.objects.create(poll=poll, option_text="Saturday Morning")
    PollOption.objects.create(poll=poll, option_text="Sunday Morning")
    PollOption.objects.create(poll=poll, option_text="Sunday Evening")
    VisitorLog.objects.create(
        name="Amazon Delivery", flat=all_flats[0], purpose="Package delivery", visitor_type="DELIVERY"
    )
    
    print("Database seeding completed! Login credentials:")
    print("  Secretary : username=secretary1  password=password123")
    print("  Resident  : username=resident1   password=password123")
    print("  Security  : username=guard1      password=password123")

if __name__ == '__main__':
    seed()
