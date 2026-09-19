import json
from django.test import Client
from admin_panel.models import ProductSetup
from users.models import PublicUserProfile, UserCartItem

print("--- STARTING CART, CHECKOUT & REVIEW BOUNDARY TESTS ---")

# 1. Setup client
client = Client()

# Get an existing product
product = ProductSetup.objects.first()
assert product is not None, "At least one product should exist in database"
print(f"Testing with product: id={product.id}, name={product.PRODUCT_NAME}, slug={product.slug}")

# 2. TEST GUEST ADD TO CART
print("\n[TEST 1] Guest Add to Cart:")
res = client.post('/cart/add/', 
    data=json.dumps({'product_id': product.id, 'quantity': 2}),
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)
print(f"Response status: {res.status_code}")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
data = res.json()
print(f"Response json: {data}")
assert data['status'] == 'success'
assert data['cart_count'] == 2

# 3. TEST GUEST VIEWING THE CART
print("\n[TEST 2] Guest Viewing the Cart (/cart/):")
res = client.get('/cart/')
print(f"Response status: {res.status_code}")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
content = res.content.decode('utf-8')
assert product.PRODUCT_NAME in content, "Product name should be present in cart page"
assert "Guest Basket Active" in content, "Guest notice should be present for anonymous user"
assert "Sign In to Proceed" in content, "Login gate button should be present for anonymous user"
print("Cart page renders correctly for guest without requiring login!")

# 4. TEST CHECKOUT ACCESS AS GUEST (MUST BE BLOCKED AND REDIRECT TO LOGIN)
print("\n[TEST 3] Checkout Access as Guest (/checkout/):")
res = client.get('/checkout/')
print(f"Response status: {res.status_code}")
assert res.status_code == 302, f"Expected 302 redirect, got {res.status_code}"
print(f"Redirect location: {res.url}")
assert '/login/' in res.url and 'next=' in res.url, f"Expected redirect to login with next param, got {res.url}"
print("Server-side gate blocked guest checkout and redirected to login with next=/checkout/!")

# 5. TEST MERGE SESSION CART ON LOGIN
print("\n[TEST 4] Session Cart Merge on Login:")
# Find or create a test PublicUserProfile
user = PublicUserProfile.objects.first()
if not user:
    user = PublicUserProfile.objects.create(
        PUBLIC_USER_FULL_NAME="Test Buyer",
        PUBLIC_USER_EMAIL="buyer@example.com",
        PUBLIC_USER_MOBILE_NO="9800000000",
        PUBLIC_USER_ADDRESS="Kathmandu, Nepal",
        PUBLIC_USER_PASSWORD="hashed_test_pass"
    )

# Clear existing UserCartItem for this user to test clean merge
UserCartItem.objects.filter(user=user).delete()

# Simulate logging in the user
session = client.session
session['public_user_id'] = user.id
session['public_user_name'] = user.PUBLIC_USER_FULL_NAME
session['role'] = 'PUBLIC_USER'
session.save()

# Trigger merge manually or via view
from core.cart import Cart
cart = Cart(client)
cart.merge_session_cart(user)

user_items = UserCartItem.objects.filter(user=user)
print(f"UserCartItem count in database after merge: {user_items.count()}")
assert user_items.filter(product=product).exists(), "Product should be merged into UserCartItem"
merged_item = user_items.get(product=product)
print(f"Merged item quantity: {merged_item.quantity}")
assert merged_item.quantity == 2, f"Expected quantity 2, got {merged_item.quantity}"

# Now test accessing checkout as authenticated user
res = client.get('/checkout/')
print(f"Authenticated user /checkout/ status: {res.status_code}")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
checkout_html = res.content.decode('utf-8')
assert user.PUBLIC_USER_FULL_NAME in checkout_html
assert product.PRODUCT_NAME in checkout_html
print("Authenticated checkout rendered successfully with merged cart items!")

# 6. TEST RATING SUBMISSION LOGIN GATE STILL HOLDS
print("\n[TEST 5] Rating/Review Submission Login Gate:")
anon_client = Client()
res = anon_client.post(f'/product/{product.slug}/', data={'rating': 5, 'comment': 'Anonymous review attempt'})
print(f"Anonymous review submission status: {res.status_code}")
# In core/views.py line 86: if not logged_in_user: redirect to login
assert res.status_code == 302, f"Expected 302 redirect for unauthenticated review, got {res.status_code}"
print(f"Review redirect URL: {res.url}")
assert '/login/' in res.url, "Should redirect unauthenticated review to login"
print("Rating submission is still securely login-gated!")

print("\n--- ALL 5 VALIDATION SUITES PASSED SUCCESSFULLY! ---")
