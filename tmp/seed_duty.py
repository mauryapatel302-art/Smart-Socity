import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsociety.settings')
django.setup()

from accounts.models import CustomUser

# Set Secretary to on duty
sec = CustomUser.objects.filter(role='SECRETARY').first()
if sec:
    sec.is_on_duty = True
    sec.save()
    print(f"Secretary {sec.username} is now ON DUTY.")

# Set first two guards to on duty
guards = CustomUser.objects.filter(role='SECURITY')[:2]
for guard in guards:
    guard.is_on_duty = True
    guard.save()
    print(f"Guard {guard.username} is now ON DUTY.")

print("Duty status update complete.")
