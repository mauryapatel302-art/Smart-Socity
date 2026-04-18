import os
import sys
import django
import argparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsociety.settings')
django.setup()

from accounts.models import CustomUser
from core.models import Wing, Flat, Notice, EmergencyContact
from billing.models import MaintenanceBill
from complaints.models import Complaint
from events.models import Event, Poll
from visitors.models import VisitorLog

def confirm_wipe(args):
    if args.confirm:
        return True
        
    print("\n" + "="*60)
    print("WARNING: DANGEROUS OPERATION")
    print("="*60)
    print("This script will completely wipe the database of all users, flags, complaints, and billing data.")
    print("This operation cannot be undone.")
    confirmation = input("Type 'YES' to confirm deletion and initialize production data: ")
    
    if confirmation.strip() == 'YES':
        return True
    return False

def init_production_db(args):
    if not confirm_wipe(args):
        print("Operation aborted by user.")
        sys.exit(0)

    print("\n[1/4] Destroying existing data...")
    CustomUser.objects.exclude(is_superuser=True).delete()
    Wing.objects.all().delete()
    Notice.objects.all().delete()
    EmergencyContact.objects.all().delete()
    Event.objects.all().delete()
    Poll.objects.all().delete()
    MaintenanceBill.objects.all().delete()
    VisitorLog.objects.all().delete()

    print("[2/4] Initializing physical society layout...")
    # 4 Wings (A, B, C, D)
    wings_data = ['A', 'B', 'C', 'D']
    wings = []
    for wing_name in wings_data:
        wings.append(Wing.objects.create(name=wing_name))
        
    # 8 Floors, 4 flats per floor (Total 128)
    total_flats = 0
    for wing in wings:
        for floor in range(1, 9): # Floors 1 to 8
            for unit in range(1, 5): # Flats 1 to 4 per floor
                # Format flat numbering natively e.g. 101, 804
                flat_number = f"{floor}0{unit}"
                Flat.objects.create(wing=wing, number=flat_number)
                total_flats += 1

    print(f"      -> Created {len(wings)} Wings and {total_flats} Flats.")

    print("[3/4] Initializing core staff accounts...")
    
    # Create Secretary
    sec, _ = CustomUser.objects.get_or_create(
        username='secretary', 
        defaults={
            'email': 'secretary@smartsociety.com', 
            'role': 'SECRETARY', 
            'first_name': 'Society', 
            'last_name': 'Secretary', 
            'phone': ''
        }
    )
    sec.set_password('password123')
    sec.save()

    # Create 3 Guards
    guard_data = [
        ('guard1', 'Main Gate', 'Guard 1', ''),
        ('guard2', 'Tower A', 'Guard 2', ''),
        ('guard3', 'Tower B', 'Guard 3', ''),
    ]
    
    guards_created = 0
    for g_user, g_first, g_last, g_phone in guard_data:
        guard, _ = CustomUser.objects.get_or_create(
            username=g_user, 
            defaults={
                'email': f'{g_user}@smartsociety.com', 
                'role': 'SECURITY', 
                'first_name': g_first, 
                'last_name': g_last, 
                'phone': g_phone
            }
        )
        guard.set_password('password123')
        guard.save()
        guards_created += 1

    print(f"      -> Created 1 Secretary and {guards_created} Guards.")
    
    print("[4/4] Finalizing setup...")
    print("\n" + "="*60)
    print("PRODUCTION DATABASE INITIALIZATION COMPLETE")
    print("="*60)
    print("Login Credentials:")
    print("  Secretary       : username=secretary   password=password123")
    print("  Security Guards : username=guard1      password=password123")
    print("                 : username=guard2      password=password123")
    print("                 : username=guard3      password=password123")
    print("\nNext Steps:")
    print("  1. Log in as 'secretary'")
    print("  2. Direct residents to sign up natively at the landing page.")
    print("============================================================")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize Production Database')
    parser.add_argument('--confirm', action='store_true', help='Skip interactive confirmation safety prompt')
    args = parser.parse_args()
    
    init_production_db(args)
