import os
import django
from django.test.client import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsociety.settings')
django.setup()

# Credentials map
users = {
    'Secretary': ('DivyarajVihol', 'Dv@12345'),
    'Resident': ('ShivamPatel', 'Sp@12345'),
    'Security': ('MauryaPatel', 'Mp@12345')
}

endpoints_no_args = [
    'dashboard',
    'profile',
    'profile_edit',
    'resident_list',
    'generate_bills',
    'my_bills',
    'billing_status',
    'complaints:list',
    'complaints:create',
    'core:notices',
    'core:create_notice',
    'core:directory',
    'events:events_list',
    'events:create_event',
    'events:polls_list',
    'events:create_poll',
    'visitors:security_dashboard',
    'visitors:create_visitor',
    'visitors:my_gate_passes',
    'visitors:create_gate_pass',
]

def check_all():
    results = {}
    for role, (username, password) in users.items():
        client = Client(SERVER_NAME='127.0.0.1')
        login_success = client.login(username=username, password=password)
        results[role] = {'login_success': login_success, 'pages': {}}
        
        if not login_success:
            results[role]['login_error'] = "Authentication failed. Incorrect username or password, or user doesn't exist."
            continue
            
        for ep in endpoints_no_args:
            try:
                url = reverse(ep)
                response = client.get(url)
                # Store status and if it's a redirect (302), check where it redirects to see if it's unauthorized
                if response.status_code == 302:
                    results[role]['pages'][ep] = f"{response.status_code} (Redirect to {response.url})"
                elif response.status_code >= 400:
                    results[role]['pages'][ep] = f"{response.status_code} Error"
                else:
                    results[role]['pages'][ep] = f"{response.status_code} OK"
            except Exception as e:
                results[role]['pages'][ep] = f"Exception: {str(e)}"
    return results

if __name__ == '__main__':
    res = check_all()
    
    with open('tmp/site_check_results.txt', 'w') as f:
        for role, data in res.items():
            f.write(f"--- ROLE: {role} ---\n")
            f.write(f"Login Success: {data['login_success']}\n")
            if data['login_success']:
                for ep, status in data['pages'].items():
                    f.write(f"  {ep.ljust(30)} : {status}\n")
            else:
                f.write(f"  Error: {data.get('login_error')}\n")
            f.write("\n")
    print("Check complete. Results saved to tmp/site_check_results.txt")
