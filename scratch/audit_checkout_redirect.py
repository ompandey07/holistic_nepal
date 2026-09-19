import os, sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
import django
django.setup()
from django.test import Client
from users.models import PublicUserProfile
from django.contrib.auth.hashers import make_password
import json

client = Client()
user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL='ashishshrestha736@gmail.com').first()
if user:
    user.PUBLIC_USER_PASSWORD = make_password('password123')
    user.save()
    login_res = client.post('/login/',
                            data=json.dumps({'email': 'ashishshrestha736@gmail.com', 'password': 'password123'}),
                            content_type='application/json')
    print('Login status:', login_res.json().get('status'))
    print('Session keys:', list(client.session.keys()))

    r = client.get('/checkout/')
    print('Checkout status:', r.status_code)
    if r.status_code in (301, 302):
        print('Redirect to:', r.get('Location', 'N/A'))

# Also check views.py CheckoutPageView auth logic
print('\n--- CheckoutPageView code ---')
from core.views import CheckoutPageView
import inspect
print(inspect.getsource(CheckoutPageView))
