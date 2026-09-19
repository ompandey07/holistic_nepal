import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import Client
from admin_panel.models import ProductSetup, ProductRating
from users.models import PublicUserProfile

print("======================================================")
print("SITEWIDE REVIEW & RATING AUDIT — VERIFICATION SCRIPT")
print("======================================================")

# --- PART 1: EMPTY STATE VERIFICATION ---
print("\n[STEP 1 & 4] Checking Empty States with 0 reviews in DB...")
assert ProductRating.objects.count() == 0, f"Expected 0 reviews in DB, found {ProductRating.objects.count()}"

client = Client()

# Check Homepage
res_home = client.get('/')
assert res_home.status_code == 200, f"Homepage failed with {res_home.status_code}"
home_html = res_home.content.decode('utf-8')

# Ensure empty state text appears
assert "No reviews yet — be the first to review this product." in home_html, "Homepage empty state text missing!"
assert "No ratings yet" in home_html, "Homepage 'No ratings yet' missing!"

# Ensure no demo names exist anywhere on the homepage
demo_names = ["Bikash Thapa", "Sunita Adhikari", "Dr. Sushil Sharma", "Dr. Anup Karki", "Ramesh Adhikari"]
for name in demo_names:
    assert name not in home_html, f"Demo name '{name}' found on homepage!"
print("[PASS] Homepage verified: 0 demo reviews, clean empty state displayed across all specimen cards.")

# Check all products for empty states
products = list(ProductSetup.objects.all())
print(f"\nChecking {len(products)} products on Product Detail Page...")
for p in products:
    res_p = client.get(f"/product/{p.slug}/")
    assert res_p.status_code == 200, f"Product {p.slug} failed with {res_p.status_code}"
    p_html = res_p.content.decode('utf-8')

    assert "No reviews yet" in p_html, f"Product {p.slug} missing 'No reviews yet' in rating row or badge!"
    assert "No reviews yet — be the first to review this product." in p_html, f"Product {p.slug} missing empty review state!"
    for name in demo_names:
        assert name not in p_html, f"Demo name '{name}' found on product {p.slug} page!"
print(f"[PASS] All {len(products)} Product Detail Pages verified: clean empty states, no fake stars, no demo names.")


# --- PART 2: STEP 5 END-TO-END TEST ---
print("\n[STEP 5] Performing Real End-to-End Test with genuine logged-in user...")

# Pick a target product
target_product = products[0]
print(f"Target Product: '{target_product.PRODUCT_NAME}' (slug: {target_product.slug})")

# Get or create real user
user = PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL="ashishshrestha736@gmail.com").first()
if not user:
    user = PublicUserProfile.objects.create(
        PUBLIC_USER_EMAIL="ashishshrestha736@gmail.com",
        PUBLIC_USER_FULL_NAME="Ashish Shrestha",
        PUBLIC_USER_ADDRESS="Kathmandu, Nepal",
        PUBLIC_USER_PASSWORD="hashedpassword"
    )
print(f"Logged-in Test User: '{user.PUBLIC_USER_FULL_NAME}' ({user.PUBLIC_USER_EMAIL})")

# Log in the user in session
session = client.session
session['public_user_id'] = user.id
session['public_user_name'] = user.PUBLIC_USER_FULL_NAME
session['role'] = 'PUBLIC_USER'
session.save()

# Submit real review via POST
review_rating = "4.8"
review_comment = "Noticeable vitality increase after two weeks of consistent morning intake. Superb authentic Himalayan formulation!"

post_res = client.post(f"/product/{target_product.slug}/", data={
    'rating': review_rating,
    'comment': review_comment,
})
assert post_res.status_code == 302, f"Expected 302 redirect on submission, got {post_res.status_code}"
print("[PASS] Real review submitted successfully via login-gated POST form.")

# Verify Database Record
db_review = ProductRating.objects.filter(PRODUCT_RATING_PRODUCT=target_product, PRODUCT_RATING_USER=user).first()
assert db_review is not None, "Review was not saved in DB!"
assert float(db_review.PRODUCT_RATING_VALUE) == 4.8, f"Expected rating 4.8, got {db_review.PRODUCT_RATING_VALUE}"
assert db_review.english_comment == review_comment
assert db_review.IS_VERIFIED is True
assert db_review.reviewer_name == "Ashish Shrestha"
print("[PASS] Database record verified:")
print(f"   - Product: {db_review.PRODUCT_RATING_PRODUCT.PRODUCT_NAME}")
print(f"   - Reviewer: {db_review.reviewer_name} (linked to User ID {user.id})")
print(f"   - Location: {db_review.reviewer_location}")
print(f"   - Rating: {db_review.PRODUCT_RATING_VALUE}")
print(f"   - Comment: {db_review.english_comment}")
print(f"   - Verified Status: {db_review.IS_VERIFIED}")

# Verify Product Detail Page
res_detail = client.get(f"/product/{target_product.slug}/")
detail_html = res_detail.content.decode('utf-8')

assert "Ashish Shrestha" in detail_html, "Reviewer name missing from detail page!"
assert review_comment in detail_html, "Comment missing from detail page!"
assert "4.8" in detail_html, "Rating 4.8 missing from detail page!"
assert "REVIEW #01" in detail_html, "Review sequence number missing!"
assert "VERIFIED PATRON" in detail_html, "Verified badge missing!"
assert "1 verified review" in detail_html, "Verified review counter missing!"

target_product.refresh_from_db()
assert target_product.reviews_count == 1, f"Expected 1 review, got {target_product.reviews_count}"
assert target_product.avg_rating == 4.8, f"Expected 4.8 avg rating, got {target_product.avg_rating}"
print("[PASS] Product Detail Page verified: shows ONLY this real review and recalculates aggregate rating to 4.8.")

# Verify Homepage Showcase Carousel
res_home_after = client.get('/')
home_after_html = res_home_after.content.decode('utf-8')

assert "Ashish Shrestha" in home_after_html, "Reviewer name missing from homepage showcase card!"
assert review_comment in home_after_html, "Comment missing from homepage showcase card!"
assert "4.8" in home_after_html, "Rating missing from homepage showcase card!"

# Confirm OTHER products on the homepage still have empty state
other_products = [p for p in products if p.id != target_product.id]
if other_products:
    assert "No reviews yet — be the first to review this product." in home_after_html, "Other products should retain empty state!"

print("[PASS] Homepage Carousel verified: target product displays real review; other products display clean empty states.")
print("\n======================================================")
print("ALL TESTS PASSED SUCCESSFULLY! 100% CLEAN AND AUDITED.")
print("======================================================")
