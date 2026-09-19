import os, sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
import django
django.setup()

from django.test import Client
from admin_panel.models import ProductSetup, ProductOrder
from users.models import PublicUserProfile
from django.contrib.auth.hashers import make_password

client = Client()
results = []

# Basic pages
for path, label in [
    ('/', 'Home'),
    ('/products/', 'Products listing'),
    ('/news/', 'News listing'),
    ('/hospital/', 'Hospital'),
    ('/gallery/', 'Gallery'),
    ('/cart/', 'Cart (unauth)'),
    ('/login/', 'Login'),
    ('/register/', 'Register'),
]:
    try:
        r = client.get(path)
        results.append((label, path, r.status_code))
    except Exception as e:
        results.append((label, path, f'EXCEPTION: {e}'))

# Checkout unauthenticated
try:
    r = client.get('/checkout/')
    results.append(('Checkout (unauth)', '/checkout/', r.status_code))
except Exception as e:
    results.append(('Checkout (unauth)', '/checkout/', f'EXCEPTION: {e}'))

# All product detail pages
slugs = list(ProductSetup.objects.values_list('PRODUCT_SLUG', flat=True))
for slug in slugs:
    try:
        r = client.get(f'/product/{slug}/')
        results.append((f'Product detail', f'/product/{slug}/', r.status_code))
    except Exception as e:
        results.append((f'Product detail', f'/product/{slug}/', f'EXCEPTION: {e}'))

# All service pages
from admin_panel.models import Service
service_slugs = list(Service.objects.values_list('slug', flat=True))
for slug in service_slugs:
    try:
        r = client.get(f'/services/{slug}/')
        results.append(('Service detail', f'/services/{slug}/', r.status_code))
    except Exception as e:
        results.append(('Service detail', f'/services/{slug}/', f'EXCEPTION: {e}'))

# All news detail pages
from admin_panel.models import News
news_slugs = list(News.objects.values_list('NEWS_SLUG', flat=True))
for slug in news_slugs:
    try:
        r = client.get(f'/news/{slug}/')
        results.append(('News detail', f'/news/{slug}/', r.status_code))
    except Exception as e:
        results.append(('News detail', f'/news/{slug}/', f'EXCEPTION: {e}'))

# Authenticated user pages - log in first
user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL='ashishshrestha736@gmail.com').first()
if user:
    user.PUBLIC_USER_PASSWORD = make_password("password123")
    user.save()
    login_res = client.post('/login/', data='{"email":"ashishshrestha736@gmail.com","password":"password123"}',
                            content_type='application/json')
    login_ok = login_res.json().get('status') == 'success'
    results.append(('Login POST', '/login/', '200+success' if login_ok else f'FAILED: {login_res.content[:100]}'))

    for path, label in [
        ('/user-side/dashboard/', 'User Dashboard'),
        ('/user-side/orders/', 'User Orders'),
        ('/user-side/settings/', 'User Settings'),
        ('/checkout/', 'Checkout (auth)'),
    ]:
        try:
            r = client.get(path)
            results.append((label, path, r.status_code))
        except Exception as e:
            results.append((label, path, f'EXCEPTION: {e}'))

# Print report
print('=' * 90)
print(f'{"Label":<30} {"Path":<45} {"Status"}')
print('=' * 90)
for label, path, code in results:
    ok = str(code) == '200' or str(code) == '200+success'
    redir = str(code) in ('301', '302')
    flag = '[OK]' if ok else ('[REDIR]' if redir else '[!!]')
    print(f'{flag:8} {label:<28} {path:<45} {code}')
print('=' * 90)
