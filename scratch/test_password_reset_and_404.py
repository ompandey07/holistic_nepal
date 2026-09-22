import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import Client
from django.core import mail
from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

from users.models import PublicUserProfile, EmployeeSetup
from security.views import public_user_token_generator, check_password_reset_rate_limit



def run_tests():
    print("=== STARTING VERIFICATION TESTS ===")
    client = Client()
    cache.clear()

    # -------------------------------------------------------------
    # 1. TEST 404 HANDLER AND TEMPLATE
    # -------------------------------------------------------------
    print("\n--- 1. Testing 404 Page & Handler ---")
    from django.conf import settings
    orig_debug = settings.DEBUG
    settings.DEBUG = False
    try:
        response = client.get('/this-path-definitely-does-not-exist-xyz/')
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        content = response.content.decode('utf-8')
        assert 'face-svg' in content, "Expected face-svg in 404 response content"
        assert 'eye-pupil' in content, "Expected eye-pupil in 404 response content"
        assert 'mouth-path' in content, "Expected mouth-path in 404 response content"
        assert '404' in content, "Expected 404 in content"
        assert 'Return to Home' in content, "Expected Return to Home button in 404 page"
        print("  [PASS] 404 handler returned 404 status and rendered animated face template!")
    finally:
        settings.DEBUG = orig_debug

    # -------------------------------------------------------------
    # 2. TEST FORGOT PASSWORD LINK IN LOGIN.HTML
    # -------------------------------------------------------------
    print("\n--- 2. Testing Login Page 'Forgot password?' Link ---")
    login_resp = client.get(reverse('login'))
    assert login_resp.status_code == 200
    login_content = login_resp.content.decode('utf-8')
    assert 'href="/password-reset/"' in login_content or 'href="/security/password-reset/"' in login_content, \
        "Expected login page to link to /password-reset/"
    assert 'Forgot password?' in login_content
    print("  [PASS] Login page has active link to password_reset route!")

    # -------------------------------------------------------------
    # 3. TEST SCOPING TO PublicUserProfile ONLY
    # -------------------------------------------------------------
    print("\n--- 3. Testing Account Scoping (PublicUserProfile vs Staff/Admin) ---")
    # Setup test employee
    emp_email = 'staff_test_security@example.com'
    EmployeeSetup.objects.filter(EMPLOYEE_EMAIL=emp_email).delete()
    emp = EmployeeSetup.objects.create(
        EMPLOYEE_FULL_NAME='Staff Tester',
        EMPLOYEE_EMAIL=emp_email,
        EMPLOYEE_PASSWORD=make_password('StaffPassword123'),
        EMPLOYEE_ADDRESS='Kathmandu',
        EMPLOYEE_ROLE='STAFF'
    )

    mail.outbox = []
    # Attempt reset with employee email
    resp = client.post(reverse('password_reset'), {'email': emp_email})
    assert resp.status_code in (200, 302), f"Expected 200 or 302, got {resp.status_code}"
    # Mail outbox should be empty because EmployeeSetup is excluded
    assert len(mail.outbox) == 0, f"Expected 0 emails for employee reset attempt, got {len(mail.outbox)}"
    print("  [PASS] Employee accounts are excluded from public self-service password reset!")

    # -------------------------------------------------------------
    # 4. TEST TOKEN GENERATION AND SINGLE-USE INVALIDATION
    # -------------------------------------------------------------
    print("\n--- 4. Testing PasswordResetTokenGenerator Behavior ---")
    customer_email = 'customer_test_reset@example.com'
    PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL=customer_email).delete()
    customer = PublicUserProfile.objects.create(
        PUBLIC_USER_FULL_NAME='Reset Customer',
        PUBLIC_USER_EMAIL=customer_email,
        PUBLIC_USER_MOBILE_NO='9800000000',
        PUBLIC_USER_ADDRESS='Pokhara, Nepal',
        PUBLIC_USER_IP='127.0.0.1',
        PUBLIC_USER_PASSWORD=make_password('InitialSecret123')
    )

    token = public_user_token_generator.make_token(customer)
    assert public_user_token_generator.check_token(customer, token) is True, "Token should be valid initially"
    
    # Check invalidation on tampered token
    assert public_user_token_generator.check_token(customer, token + 'tamper') is False, "Tampered token should be invalid"

    # Invalidation on password change
    customer.PUBLIC_USER_PASSWORD = make_password('NewPassword456')
    customer.save()
    assert public_user_token_generator.check_token(customer, token) is False, \
        "Old token must become invalid immediately after password change!"
    print("  [PASS] Token validates correctly and immediately invalidates upon password modification!")

    # -------------------------------------------------------------
    # 5. TEST RATE LIMITING
    # -------------------------------------------------------------
    print("\n--- 5. Testing Rate Limiting (max 5 requests per hour) ---")
    test_ip = '192.168.100.99'
    rate_email = 'ratelimit_customer@example.com'
    # First 5 calls should succeed
    for i in range(5):
        limited = check_password_reset_rate_limit(test_ip, rate_email, limit=5, timeout=3600)
        assert limited is False, f"Attempt {i+1} should not be rate limited"

    # 6th call should be blocked
    limited = check_password_reset_rate_limit(test_ip, rate_email, limit=5, timeout=3600)
    assert limited is True, "6th attempt must be rate limited!"

    # Test via view
    resp_limited = client.post(
        reverse('password_reset'),
        data={'email': rate_email},
        REMOTE_ADDR=test_ip,
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert resp_limited.status_code == 429, f"Expected HTTP 429, got {resp_limited.status_code}"
    print("  [PASS] Rate limiting strictly blocks more than 5 requests per hour!")

    # -------------------------------------------------------------
    # 6. TEST FULL END-TO-END CUSTOMER PASSWORD RESET FLOW
    # -------------------------------------------------------------
    print("\n--- 6. Testing Complete End-to-End Reset & Login Flow ---")
    cache.clear()
    mail.outbox = []

    # Reset customer password back to a known value
    customer.PUBLIC_USER_PASSWORD = make_password('InitialPassword123')
    customer.save()

    # Step A: Request password reset
    req_resp = client.post(
        reverse('password_reset'),
        {'email': customer.PUBLIC_USER_EMAIL},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert req_resp.status_code == 200, f"Expected 200, got {req_resp.status_code}"
    assert len(mail.outbox) == 1, f"Expected 1 email sent, got {len(mail.outbox)}"
    sent_email = mail.outbox[0]
    assert customer.PUBLIC_USER_EMAIL in sent_email.to
    assert 'password-reset/confirm' in sent_email.body
    print("  [PASS] Step A: Reset request sent email with confirmation link.")

    # Step B: Extract token and uidb64
    uidb64 = urlsafe_base64_encode(force_bytes(customer.pk))
    fresh_token = public_user_token_generator.make_token(customer)
    confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': fresh_token})

    # Step C: Visit confirm page (GET)
    confirm_get = client.get(confirm_url)
    assert confirm_get.status_code == 200
    assert 'Set New Password' in confirm_get.content.decode('utf-8')
    assert 'Change Password' in confirm_get.content.decode('utf-8')
    print("  [PASS] Step B: Confirm page renders valid form for fresh token.")

    # Step D: Submit new password (POST)
    new_pass = 'MySuperNewSafePassword2026!'
    confirm_post = client.post(
        confirm_url,
        {'password': new_pass, 'confirm_password': new_pass},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert confirm_post.status_code == 200
    customer.refresh_from_db()
    assert check_password(new_pass, customer.PUBLIC_USER_PASSWORD) is True, \
        "PublicUserProfile password was not updated with new password!"
    print("  [PASS] Step C: Password successfully updated in PublicUserProfile!")

    # Step E: Log in with new password
    login_attempt = client.post(
        reverse('login'),
        {'email': customer.PUBLIC_USER_EMAIL, 'password': new_pass},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert login_attempt.status_code == 200, f"Expected 200, got {login_attempt.status_code}"
    login_data = login_attempt.json()
    assert login_data['status'] == 'success', f"Expected success status, got {login_data}"
    print("  [PASS] Step D: Customer successfully logged in using new password!")

    # Clean up test records
    emp.delete()
    customer.delete()
    print("\n=== ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    run_tests()
