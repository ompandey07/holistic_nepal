import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holistic_nepal.settings')
django.setup()

from django.test import Client
from admin_panel.models import ProductSetup, ProductRating
from users.models import PublicUserProfile

print("=== STEP 4: REAL REVIEW SUBMISSION & CAROUSEL TEST ===")

# 1. Target product: ashish item (slug: ashish-item)
product = ProductSetup.objects.get(PRODUCT_SLUG='ashish-item')
print(f"Product: id={product.id}, name='{product.PRODUCT_NAME}', slug='{product.slug}'")

# Before: Initial count of real reviews for this product
initial_reviews = list(product.PRODUCT_RATINGS.all())
print(f"Initial real reviews for this product: {len(initial_reviews)}")
for r in initial_reviews:
    print(f" - {r.reviewer_name} ({r.reviewer_location}): {r.PRODUCT_RATING_VALUE} stars - '{r.english_comment}'")

client = Client()

# Check public view before submission
res = client.get(f'/product/{product.slug}/')
assert res.status_code == 200
content_before = res.content.decode('utf-8')
# Confirm Sunita Adhikari is NOT in this product's carousel anymore (she belongs to product 27)
assert "Sunita Adhikari" not in content_before, "Sunita Adhikari should NOT appear on ashish-item"
print("Confirmed: Foreign product review (Sunita Adhikari) is no longer showing on ashish-item!")

# 2. Setup real test user
test_user, _ = PublicUserProfile.objects.get_or_create(
    PUBLIC_USER_EMAIL="anil.karki@example.com",
    defaults={
        'PUBLIC_USER_FULL_NAME': "Anil Karki",
        'PUBLIC_USER_MOBILE_NO': "9841234567",
        'PUBLIC_USER_ADDRESS': "Patan, Lalitpur, Nepal",
        'PUBLIC_USER_PASSWORD': "testpassword123"
    }
)
# Clean any previous review by test user on this product to ensure clean test
ProductRating.objects.filter(PRODUCT_RATING_PRODUCT=product, PRODUCT_RATING_USER=test_user).delete()

# 3. Log in test user in session
session = client.session
session['public_user_id'] = test_user.id
session['public_user_name'] = test_user.PUBLIC_USER_FULL_NAME
session['role'] = 'PUBLIC_USER'
session.save()

# 4. Submit real review via POST
submission_comment = "Excellent traditional Ayurvedic quality. Noticed improved vigor and vitality after three weeks."
post_res = client.post(f'/product/{product.slug}/', data={
    'rating': '4.0',
    'comment': submission_comment
})
print(f"\nSubmission POST status code: {post_res.status_code}")
assert post_res.status_code == 302, f"Expected 302 redirect, got {post_res.status_code}"
assert f"/product/{product.slug}/" in post_res.url

# 5. Verify database record
new_review = ProductRating.objects.filter(PRODUCT_RATING_PRODUCT=product, PRODUCT_RATING_USER=test_user).first()
assert new_review is not None, "New review record should exist in database"
print(f"Database Record Created:")
print(f" - Reviewer: {new_review.reviewer_name}")
print(f" - Location: {new_review.reviewer_location}")
print(f" - Rating Value: {new_review.PRODUCT_RATING_VALUE}")
print(f" - Rating Stars (length): {len(new_review.rating_stars)}")
print(f" - Comment: {new_review.english_comment}")
print(f" - Is Verified: {new_review.IS_VERIFIED}")
print(f" - Created At: {new_review.PRODUCT_RATING_CREATED_AT}")

assert new_review.reviewer_name == "Anil Karki"
assert "Patan, Lalitpur" in new_review.reviewer_location
assert float(new_review.PRODUCT_RATING_VALUE) == 4.0
assert new_review.english_comment == submission_comment
assert new_review.IS_VERIFIED is True

# 6. Verify GET page rendering with the new review
res_after = client.get(f'/product/{product.slug}/')
assert res_after.status_code == 200
html = res_after.content.decode('utf-8')

assert "Anil Karki" in html, "Reviewer name 'Anil Karki' must be in HTML"
assert "Patan, Lalitpur" in html, "Reviewer location must be in HTML"
assert submission_comment in html, "Reviewer comment must be in HTML"
assert "4.0" in html, "Rating 4.0 must be in HTML"
assert "REVIEW #01" in html, "Position numbering must be present"
assert "VERIFIED PATRON" in html, "Verified badge must be present"

# Aggregate checks: (5.0 + 4.0) / 2 = 4.5
product.refresh_from_db()
print(f"\nUpdated Aggregate Metrics:")
print(f" - Total Reviews: {product.reviews_count}")
print(f" - Average Rating: {product.avg_rating}")
print(f" - Star String (length): {len(product.avg_rating_stars)}")

assert product.reviews_count == 2, f"Expected 2 reviews, got {product.reviews_count}"
assert product.avg_rating == 4.5, f"Expected avg 4.5, got {product.avg_rating}"

assert "2 verified reviews" in html, "'2 verified reviews' must be displayed"
assert "4.5" in html, "Aggregate rating '4.5' must be displayed"

print("\n=== ALL TEST VERIFICATIONS PASSED 100%! ===")
