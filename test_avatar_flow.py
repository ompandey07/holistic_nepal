import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import Client
from users.models import PublicUserProfile

print("=== TESTING NAVBAR ACCOUNT & AVATAR COMPONENT ===")

client = Client()

# [SCENARIO 1] Guest State (Not logged in)
print("\n[TEST 1] Guest State Navbar:")
res_guest = client.get('/')
assert res_guest.status_code == 200
html_guest = res_guest.content.decode('utf-8')

assert 'nav-guest-btn' in html_guest, "Guest avatar button with 'nav-guest-btn' must be present"
assert 'nav-user-icon' in html_guest, "Outline user SVG icon must be present"
assert 'href="/security/login/"' in html_guest or 'href="/login/"' in html_guest, "Guest icon must link to login"
assert 'Patron Account' in html_guest, "Guest dropdown title must be present"
assert 'Sign In' in html_guest, "Dropdown Sign In link must be present"
assert 'Create Account' in html_guest, "Dropdown Create Account link must be present"
print("[PASS] Guest state correctly renders grey outline person icon linking to login with dropdown!")

# [SCENARIO 2] Logged-in User WITHOUT Profile Photo
print("\n[TEST 2] Logged-in User WITHOUT Profile Photo:")
user_no_photo, _ = PublicUserProfile.objects.get_or_create(
    PUBLIC_USER_EMAIL="ashish.noimage@example.com",
    defaults={
        'PUBLIC_USER_FULL_NAME': "Ashish Sharma",
        'PUBLIC_USER_MOBILE_NO': "9811111111",
        'PUBLIC_USER_ADDRESS': "Kathmandu, Nepal",
        'PUBLIC_USER_PASSWORD': "testpassword"
    }
)
user_no_photo.PUBLIC_USER_PROFILE_IMAGE = None
user_no_photo.save()

session = client.session
session['public_user_id'] = user_no_photo.id
session['public_user_name'] = user_no_photo.PUBLIC_USER_FULL_NAME
session['role'] = 'PUBLIC_USER'
session.save()

res_no_photo = client.get('/')
assert res_no_photo.status_code == 200
html_no_photo = res_no_photo.content.decode('utf-8')

assert 'nav-user-avatar-btn' in html_no_photo, "'nav-user-avatar-btn' must be present"
assert 'nav-avatar-initial' in html_no_photo, "'nav-avatar-initial' must be present"
assert '>A<</span>' in html_no_photo or '>A<' in html_no_photo, "Avatar initial 'A' must be rendered"
assert 'nav-avatar-photo' not in html_no_photo, "Image tag should NOT be rendered when no photo exists"
assert "Ashish Sharma" in html_no_photo, "User name must be in dropdown"
assert "My Dashboard" in html_no_photo, "'My Dashboard' must be in dropdown"
assert "Log Out" in html_no_photo, "'Log Out' must be in dropdown"
print("[PASS] Logged-in user without photo renders circular avatar with initial 'A' and full account menu!")

# [SCENARIO 3] Logged-in User WITH Profile Photo
print("\n[TEST 3] Logged-in User WITH Profile Photo:")
from django.core.files.uploadedfile import SimpleUploadedFile
small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
    b'\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
    b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
)

user_with_photo, _ = PublicUserProfile.objects.get_or_create(
    PUBLIC_USER_EMAIL="bikash.withimage@example.com",
    defaults={
        'PUBLIC_USER_FULL_NAME': "Bikash Thapa",
        'PUBLIC_USER_MOBILE_NO': "9822222222",
        'PUBLIC_USER_ADDRESS': "Pokhara, Nepal",
        'PUBLIC_USER_PASSWORD': "testpassword"
    }
)
user_with_photo.PUBLIC_USER_PROFILE_IMAGE.save("test_avatar.gif", SimpleUploadedFile("test_avatar.gif", small_gif, content_type="image/gif"), save=True)

session['public_user_id'] = user_with_photo.id
session['public_user_name'] = user_with_photo.PUBLIC_USER_FULL_NAME
session.save()

res_with_photo = client.get('/')
assert res_with_photo.status_code == 200
html_with_photo = res_with_photo.content.decode('utf-8')

assert 'nav-user-avatar-btn' in html_with_photo, "'nav-user-avatar-btn' must be present"
assert 'nav-avatar-photo' in html_with_photo, "Image tag with 'nav-avatar-photo' must be rendered"
assert 'test_avatar' in html_with_photo, "Image src must point to the uploaded avatar"
assert "Bikash Thapa" in html_with_photo, "User name must be in dropdown"
print("[PASS] Logged-in user with photo renders circular cropped photo in navbar!")

# Also verify on other pages (products, product_detail, cart)
print("\n[TEST 4] Verify on Other Pages:")
for path in ['/products/', '/cart/', '/product/ashish-item/']:
    res = client.get(path)
    assert res.status_code == 200, f"Expected 200 on {path}, got {res.status_code}"
    html = res.content.decode('utf-8')
    assert 'nav-user-avatar-btn' in html, f"Account avatar must appear on {path}"
    print(f"[PASS] Verified account avatar renders on {path}")

print("\n=== ALL 4 NAVBAR ACCOUNT TESTS PASSED 100%! ===")
