import os
import sys
import django
import json

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import Client
from django.contrib.auth.hashers import make_password
from users.models import PublicUserProfile, UserCartItem
from admin_panel.models import ProductOrder, ProductSetup

client = Client()

print("--- 1. Testing Unauthenticated Access to Checkout POST ---")
res_unauth = client.post('/checkout/', data=json.dumps({'full_name': 'Anonymous'}), content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"Unauthenticated status: {res_unauth.status_code}")
assert res_unauth.status_code in (401, 302), f"Expected 401 or 302, got {res_unauth.status_code}"
print("Unauthenticated check passed.")

print("\n--- 2. Setting up Authenticated Session for Test User ---")
user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL='ashishshrestha736@gmail.com').first()
if not user:
    user = PublicUserProfile.objects.create(
        PUBLIC_USER_FULL_NAME="Ashish Shrestha",
        PUBLIC_USER_EMAIL="ashishshrestha736@gmail.com",
        PUBLIC_USER_MOBILE_NO="9800000000",
        PUBLIC_USER_ADDRESS="Kathmandu, Nepal",
        PUBLIC_USER_STATUS=True
    )
# Ensure password is set with make_password
user.PUBLIC_USER_PASSWORD = make_password("password123")
user.save()

# Login via client
login_res = client.post('/login/', data=json.dumps({
    'email': 'ashishshrestha736@gmail.com',
    'password': 'password123'
}), content_type='application/json')
print(f"Login status: {login_res.status_code}, response: {login_res.json()}")
assert login_res.json().get('status') == 'success'

# Find or ensure a ProductSetup exists
prod = ProductSetup.objects.first()
if not prod:
    prod = ProductSetup.objects.create(
        PRODUCT_NAME="Triphala Churna Premium",
        PRODUCT_PRICE=450,
        PRODUCT_CONTAIN="100g Powder",
        PRODUCT_STATUS=True
    )

print(f"Using test product: {prod.PRODUCT_NAME} (ID: {prod.id}, Price: Rs {prod.PRODUCT_PRICE})")

# Clear cart first
UserCartItem.objects.filter(user=user).delete()
s = client.session
s['cart'] = {}
s.save()

print("\n--- 3. Testing POST /checkout/ with Empty Cart ---")
res_empty = client.post(
    '/checkout/',
    data=json.dumps({
        'full_name': user.PUBLIC_USER_FULL_NAME,
        'mobile_no': user.PUBLIC_USER_MOBILE_NO,
        'address': user.PUBLIC_USER_ADDRESS,
        'payment_method': 'COD'
    }),
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)
print(f"Empty cart status: {res_empty.status_code}, response: {res_empty.json()}")
assert res_empty.status_code == 400
assert res_empty.json()['status'] == 'error'
print("Empty cart rejection passed.")

print("\n--- 4. Adding Item to Cart ---")
add_res = client.post('/cart/add/', data={'product_id': prod.id, 'quantity': 2})
print(f"Add to cart status: {add_res.status_code}, cart items count in db: {UserCartItem.objects.filter(user=user).count()}")

print("\n--- 5. Testing POST /checkout/ with Validation Failure (Missing Address) ---")
res_bad = client.post(
    '/checkout/',
    data=json.dumps({
        'full_name': user.PUBLIC_USER_FULL_NAME,
        'mobile_no': user.PUBLIC_USER_MOBILE_NO,
        'address': '',
        'payment_method': 'COD'
    }),
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)
print(f"Missing address status: {res_bad.status_code}, response: {res_bad.json()}")
assert res_bad.status_code == 400
assert res_bad.json()['status'] == 'error'
print("Missing address rejection passed.")

print("\n--- 6. Submitting Real Valid Order via POST /checkout/ ---")
res_valid = client.post(
    '/checkout/',
    data=json.dumps({
        'full_name': 'Ashish Shrestha',
        'email': 'ashishshrestha736@gmail.com',
        'mobile_no': '9841234567',
        'address': 'Lazimpat, Kathmandu 44600',
        'delivery_instructions': 'Please ring the front bell on arrival',
        'payment_method': 'COD'
    }),
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)
print(f"Valid order status: {res_valid.status_code}")
data = res_valid.json()
print("Response data:", json.dumps(data, indent=2))
assert res_valid.status_code == 200
assert data['status'] == 'success'
order_id = data['order_id']
print(f"Generated Order ID: {order_id}")

print("\n--- 7. Verifying ProductOrder in Database ---")
order = ProductOrder.objects.filter(PRODUCT_ORDER_ID=order_id).first()
assert order is not None, "Order record not found in database!"
print(f"Found order: ID={order.PRODUCT_ORDER_ID}, Customer={order.CUSTOMER.PUBLIC_USER_FULL_NAME}")
print(f"Total Amount: Rs {order.TOTAL_AMOUNT}, Shipping Fee: Rs {order.SHIPPING_FEE}")
print(f"Shipping Address: {order.SHIPPING_ADDRESS}, Phone: {order.SHIPPING_PHONE}")
print(f"Payment Method: {order.PAYMENT_METHOD}, Order Source: {order.ORDER_SOURCE}")
print(f"Order Items Snapshot: {order.ORDER_ITEMS_DATA}")
print(f"Cart cleared in db? Remaining user cart items: {UserCartItem.objects.filter(user=user).count()}")
assert UserCartItem.objects.filter(user=user).count() == 0, "Cart was not cleared!"

print("\n--- 8. Verifying User Dashboard Orders View (/user-side/orders/) ---")
orders_page = client.get('/user-side/orders/')
print(f"Orders page status: {orders_page.status_code}")
assert orders_page.status_code == 200
assert order.PRODUCT_ORDER_ID.encode() in orders_page.content, f"{order.PRODUCT_ORDER_ID} not rendered in orders page!"
print("Order found in user orders page HTML!")

print("\n--- 9. Verifying User Dashboard Overview (/user-side/dashboard/) ---")
dashboard_page = client.get('/user-side/dashboard/')
print(f"Dashboard page status: {dashboard_page.status_code}")
assert dashboard_page.status_code == 200
assert order.PRODUCT_ORDER_ID.encode() in dashboard_page.content, "Order ID not found in dashboard HTML!"
print("Found order ID in dashboard recent orders list!")
if dashboard_page.context:
    if isinstance(dashboard_page.context, list):
        for c in dashboard_page.context:
            if 'order_stats' in c:
                print("Dashboard order_stats:", c['order_stats'])
    elif hasattr(dashboard_page.context, 'get'):
        print("Dashboard order_stats:", dashboard_page.context.get('order_stats'))
print("User Dashboard KPI stats verified!")

print("\nALL REAL CHECKOUT AND DASHBOARD ORDERS TESTS PASSED SUCCESSFULLY!")
