import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import RequestFactory
from core.views import OurProductsPageView
import re

rf = RequestFactory()

# test with category=beverages
req = rf.get('/products/?category=beverages')
res = OurProductsPageView()(req)
content = res.content.decode('utf-8')

sections = re.findall(r'<section class="category-group-section([^"]*)" id="cat-([^"]*)"', content)
print("With ?category=beverages:")
for cls, cat_id in sections:
    print(f"  cat-{cat_id}: classes='{cls.strip()}'")

# test with ?category=all
req_all = rf.get('/products/?category=all')
res_all = OurProductsPageView()(req_all)
content_all = res_all.content.decode('utf-8')
sections_all = re.findall(r'<section class="category-group-section([^"]*)" id="cat-([^"]*)"', content_all)
print("\nWith ?category=all:")
for cls, cat_id in sections_all:
    print(f"  cat-{cat_id}: classes='{cls.strip()}'")

# test default /products/
req_def = rf.get('/products/')
res_def = OurProductsPageView()(req_def)
content_def = res_def.content.decode('utf-8')
sections_def = re.findall(r'<section class="category-group-section([^"]*)" id="cat-([^"]*)"', content_def)
print("\nWith /products/:")
for cls, cat_id in sections_def:
    print(f"  cat-{cat_id}: classes='{cls.strip()}'")
