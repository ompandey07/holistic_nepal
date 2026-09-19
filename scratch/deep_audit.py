import os, sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
import django
django.setup()

# 1. Check products_data for missing attribute issues
from core.products_data import get_all_products
prods = get_all_products()
print('Total products from get_all_products():', len(prods))
attrs_to_check = ['name', 'slug', 'price', 'rating', 'image', 'reviews_count', 'reviews']
for p in prods:
    missing = [a for a in attrs_to_check if not hasattr(p, a)]
    if missing:
        pname = getattr(p, 'name', 'Unknown')
        print('  MISSING ATTRS on', pname, ':', missing)
if not any(True for p in prods if [a for a in attrs_to_check if not hasattr(p, a)]):
    print('All products OK - no missing attributes')

# 2. Check cart view - can empty cart reach checkout?
from core.cart import Cart
from django.test import RequestFactory
factory = RequestFactory()
req = factory.get('/cart/')
req.session = {}
cart = Cart(req)
print('\nEmpty cart items:', cart.get_items())
print('Empty cart total:', cart.get_total_price())

# 3. Check what session key the login sets
from users.models import PublicUserProfile
from django.contrib.auth.hashers import make_password, check_password
user = PublicUserProfile.objects.first()
print('\nPublicUserProfile fields:', [f.name for f in PublicUserProfile._meta.get_fields()])

# 4. Check ProductOrder model fields
from admin_panel.models import ProductOrder
print('\nProductOrder fields:', [f.name for f in ProductOrder._meta.get_fields()])

# 5. Check 404 handler
import holistic_nepal.urls as main_urls
print('\n404 handler defined:', hasattr(main_urls, 'handler404'))

# 6. Check for password reset URL
from django.urls import reverse, NoReverseMatch
for name in ['password_reset', 'password_reset_done', 'accounts:password_reset', 'reset_password']:
    try:
        url = reverse(name)
        print('Password reset URL:', name, '->', url)
    except NoReverseMatch:
        print('No route for:', name)

# 7. Check service pages
from admin_panel.models import Service
services = Service.objects.all()
print('\nService count:', services.count())
for svc in services:
    print(' -', svc.slug, '|', getattr(svc, 'name', getattr(svc, 'SERVICE_NAME', 'N/A')))

# 8. Check Gallery model and data
from admin_panel.models import Gallery, GalleryImage
albums = Gallery.objects.all()
print('\nGallery albums count:', albums.count())
for album in albums:
    imgs = GalleryImage.objects.filter(album=album).count()
    print(' - album:', album.title, '| images:', imgs)

# 9. Check News model
from admin_panel.models import News
news = News.objects.all()
print('\nNews articles count:', news.count())
for n in news:
    print(' -', n.NEWS_SLUG, '| title:', n.NEWS_TITLE[:40] if n.NEWS_TITLE else 'N/A')
