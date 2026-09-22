from users.models import EmployeeSetup , PublicUserProfile
from django.utils import timezone
from django.db import models
from django.utils.text import slugify


#!--- GALLERY MODEL -------
class Gallery(models.Model):
    GALLERY_TITLE = models.CharField(max_length=500)
    GALLERY_SLUG = models.SlugField(max_length=500, unique=True, blank=True)
    GALLERY_IMAGE = models.ImageField(upload_to="Uploads/Gallary/", null=True, blank=True)
    GALLERY_DESCRIPTION = models.TextField()
    GALLERY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_CREATED_BY", null=True, blank=True)
    GALLERY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_MODIFIED_BY", null=True, blank=True)
    GALLERY_CREATED_AT = models.DateTimeField(default=timezone.now)
    GALLERY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GALLERY"

    def save(self, *args, **kwargs):
        if not self.GALLERY_SLUG:
            orig_slug = slugify(self.GALLERY_TITLE, allow_unicode=True)
            if not orig_slug:
                orig_slug = f"gallery-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            slug = orig_slug
            counter = 1
            while Gallery.objects.filter(GALLERY_SLUG=slug).exclude(id=self.id).exists():
                slug = f"{orig_slug}-{counter}"
                counter += 1
            self.GALLERY_SLUG = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.GALLERY_TITLE


# !--- GALLERY MULTIPLE IMAGES MODEL -------
class GalleryImage(models.Model):
    GALLERY = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="GALLERY_IMAGES")
    IMAGE = models.ImageField(upload_to="Uploads/Gallary/")
    CREATED_AT = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "GALLERY IMAGE"

    def __str__(self):
        return f"Image for {self.GALLERY.GALLERY_TITLE}"



# !--- NEWS MODEL -------
class News(models.Model):
    NEWS_TYPE = models.CharField(max_length=50, choices=[
        ("ANNOUNCEMENT", "Announcement"),
        ("CERTIFICATION", "Certification"),
        ("UPDATE", "Update"),
        ("EVENT", "Event"),
        ("PRESS", "Press"),
        ("NOTICE", "Notice"),
        ("GENERAL", "General"),
    ], default="ANNOUNCEMENT")
    NEWS_TITLE = models.CharField(max_length=500)
    NEWS_SLUG = models.SlugField(max_length=500, unique=True, blank=True)
    NEWS_IMAGE = models.ImageField(upload_to="Uploads/News/", blank=True, null=True)
    NEWS_DESCRIPTION = models.TextField()
    NEWS_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="NEWS_CREATED_BY", blank=True, null=True)
    NEWS_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="NEWS_MODIFIED_BY", blank=True, null=True)
    NEWS_CREATED_AT = models.DateTimeField(default=timezone.now)
    NEWS_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "NEWS"

    def save(self, *args, **kwargs):
        if not self.NEWS_SLUG:
            orig_slug = slugify(self.NEWS_TITLE, allow_unicode=True)
            if not orig_slug:
                orig_slug = f"news-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            slug = orig_slug
            counter = 1
            while News.objects.filter(NEWS_SLUG=slug).exclude(id=self.id).exists():
                slug = f"{orig_slug}-{counter}"
                counter += 1
            self.NEWS_SLUG = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.NEWS_TITLE

    @property
    def slug(self):
        if self.NEWS_SLUG:
            return self.NEWS_SLUG
        s = slugify(self.NEWS_TITLE)
        if s:
            return s
        return f"news-{self.id or 'item'}"

    @property
    def image_url(self):
        if self.NEWS_IMAGE:
            try:
                return self.NEWS_IMAGE.url
            except Exception:
                return f"/media/{self.NEWS_IMAGE}"
        try:
            first_img = self.NEWS_IMAGES.first()
            if first_img and first_img.IMAGE:
                try:
                    return first_img.IMAGE.url
                except Exception:
                    return f"/media/{first_img.IMAGE}"
        except Exception:
            pass
        return ""


# !--- NEWS MULTIPLE IMAGES MODEL -------
class NewsImage(models.Model):
    NEWS = models.ForeignKey(News, on_delete=models.CASCADE, related_name="NEWS_IMAGES")
    IMAGE = models.ImageField(upload_to="Uploads/News/")
    CREATED_AT = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "NEWS IMAGE"

    def __str__(self):
        return f"Image for {self.NEWS.NEWS_TITLE}"

    @property
    def image_url(self):
        if self.IMAGE:
            try:
                return self.IMAGE.url
            except Exception:
                return f"/media/{self.IMAGE}"
        return ""



#!--- UNIT SETUP MODEL -------
class UnitSetup(models.Model):
    UNIT_NAME = models.CharField(max_length=200)
    UNIT_SYMBOL = models.CharField(max_length=50)
    UNIT_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="UNIT_CREATED_BY")
    UNIT_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="UNIT_MODIFIED_BY")
    UNIT_CREATED_AT = models.DateTimeField(default=timezone.now)
    UNIT_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UNIT SETUP"

    def __str__(self):
        return self.UNIT_NAME


#!--- PRODUCT CATEGORY MODEL -------
class ProductCategory(models.Model):
    CATEGORY_NAME = models.CharField(max_length=200)
    CATEGORY_TAG = models.CharField(max_length=150, null=True, blank=True, help_text="Highlight badge/tag (e.g. 'HEALTH & IMMUNITY', 'TEAS & INFUSIONS')")
    CATEGORY_IMAGE = models.ImageField(upload_to="Uploads/Category Images/", null=True, blank=True)
    CATEGORY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="CATEGORY_CREATED_BY")
    CATEGORY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="CATEGORY_MODIFIED_BY")
    CATEGORY_CREATED_AT = models.DateTimeField(default=timezone.now)
    CATEGORY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT CATEGORY"

    def __str__(self):
        return self.CATEGORY_NAME

    @property
    def slug(self):
        return slugify(self.CATEGORY_NAME)


# !--- PRODUCT SETUP MODEL -------
class ProductSetup(models.Model):
    PRODUCT_NAME = models.CharField(max_length=300)
    PRODUCT_SLUG = models.SlugField(max_length=500, unique=True, blank=True)
    PRODUCT_UNIT = models.ForeignKey(UnitSetup, on_delete=models.PROTECT, related_name="PRODUCT_UNIT")
    PRODUCT_CATEGORY = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="PRODUCT_CATEGORY")
    PRODUCT_PRICE = models.DecimalField(max_digits=15, decimal_places=2)
    PRODUCT_SIZE = models.CharField(max_length=200, null=True, blank=True)
    PRODUCT_WEIGHT = models.CharField(max_length=100, null=True, blank=True)
    PRODUCT_DESCRIPTION = models.TextField()
    PRODUCT_KEY_FEATURES = models.TextField(null=True, blank=True)
    PRODUCT_IMAGE = models.ImageField(upload_to="Uploads/Product Images/", null=True, blank=True)
    PRODUCT_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_CREATED_BY")
    PRODUCT_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_MODIFIED_BY")
    PRODUCT_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT SETUP"

    def save(self, *args, **kwargs):
        if not self.PRODUCT_SLUG:
            orig_slug = slugify(self.PRODUCT_NAME, allow_unicode=True)
            if not orig_slug:
                orig_slug = f"product-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            slug = orig_slug
            counter = 1
            while ProductSetup.objects.filter(PRODUCT_SLUG=slug).exclude(id=self.id).exists():
                slug = f"{orig_slug}-{counter}"
                counter += 1
            self.PRODUCT_SLUG = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.PRODUCT_NAME

    @property
    def slug(self):
        return self.PRODUCT_SLUG or slugify(self.PRODUCT_NAME)

    @property
    def detail_url(self):
        return f"/product/{self.slug}/"

    @property
    def name(self):
        return self.PRODUCT_NAME

    @property
    def price_formatted(self):
        try:
            val = float(self.PRODUCT_PRICE)
            return f"Rs {val:,.2f}"
        except Exception:
            return f"Rs {self.PRODUCT_PRICE}"

    @property
    def price_display(self):
        try:
            val = float(self.PRODUCT_PRICE)
            if val.is_integer():
                return f"Rs {int(val):,}"
            return f"Rs {val:,.2f}"
        except Exception:
            return f"Rs {self.PRODUCT_PRICE}"

    @property
    def short_desc(self):
        if self.PRODUCT_DESCRIPTION:
            from django.utils.html import strip_tags
            import html
            clean = html.unescape(strip_tags(self.PRODUCT_DESCRIPTION)).replace('\xa0', ' ').strip()
            return clean[:140] + ("..." if len(clean) > 140 else "")
        return ""

    @property
    def weight_or_size(self):
        return self.PRODUCT_SIZE or self.PRODUCT_WEIGHT or (self.PRODUCT_UNIT.UNIT_NAME if self.PRODUCT_UNIT else "")

    @property
    def avg_rating(self):
        ratings = self.PRODUCT_RATINGS.all()
        if ratings.exists():
            return round(sum([float(r.PRODUCT_RATING_VALUE) for r in ratings]) / ratings.count(), 1)
        return None

    @property
    def avg_rating_stars(self):
        score = self.avg_rating
        if not score:
            return ""
        full = int(score)
        half = 1 if (score - full) >= 0.5 else 0
        empty = 5 - full - half
        return ("★" * full) + ("½" if half else "") + ("☆" * empty)

    @property
    def reviews_count(self):
        try:
            return self.PRODUCT_RATINGS.count()
        except Exception:
            return 0

    @property
    def english_desc(self):
        return self.PRODUCT_DESCRIPTION or ""

    @property
    def nepali_desc(self):
        return self.PRODUCT_DESCRIPTION or ""

    @property
    def showcase_review(self):
        try:
            return self.PRODUCT_RATINGS.order_by('-id').first()
        except Exception:
            return None

    @property
    def image_url(self):
        if self.PRODUCT_IMAGE:
            try:
                return self.PRODUCT_IMAGE.url
            except Exception:
                return f"/media/{self.PRODUCT_IMAGE}"
        try:
            first_img = self.PRODUCT_IMAGES.first()
            if first_img and first_img.IMAGE:
                return first_img.IMAGE.url
        except Exception:
            pass
        return "/static/Images/fresh_herbs_extracted.png"

    @property
    def category(self):
        if self.PRODUCT_CATEGORY:
            return self.PRODUCT_CATEGORY.CATEGORY_NAME
        return "Herbal Products"

    @property
    def price(self):
        try:
            return float(self.PRODUCT_PRICE)
        except Exception:
            return 0.0



# !--- PRODUCT MULTIPLE IMAGES MODEL -------
class ProductImage(models.Model):
    PRODUCT = models.ForeignKey(ProductSetup, on_delete=models.CASCADE, related_name="PRODUCT_IMAGES")
    IMAGE = models.ImageField(upload_to="Uploads/Product Images/")
    CREATED_AT = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "PRODUCT IMAGE"

    def __str__(self):
        return f"Image for {self.PRODUCT.PRODUCT_NAME}"


# !--- PRODUCT RATING MODEL -------
class ProductRating(models.Model):
    PRODUCT_RATING_PRODUCT = models.ForeignKey(ProductSetup, on_delete=models.CASCADE, related_name="PRODUCT_RATINGS")
    PRODUCT_RATING_USER = models.ForeignKey(PublicUserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_RATINGS")
    PRODUCT_RATING_VALUE = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    PRODUCT_RATING_COMMENT = models.TextField(null=True, blank=True)
    COMMENT_ENG = models.TextField(null=True, blank=True)
    COMMENT_NEP = models.TextField(null=True, blank=True)
    REVIEWER_NAME = models.CharField(max_length=200, null=True, blank=True)
    REVIEWER_LOCATION = models.CharField(max_length=200, null=True, blank=True)
    IS_FEATURED = models.BooleanField(default=False)
    IS_VERIFIED = models.BooleanField(default=True)
    PRODUCT_RATING_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_RATING_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT RATING"
        ordering = ["-IS_FEATURED", "-PRODUCT_RATING_CREATED_AT"]

    def __str__(self):
        return f"{self.PRODUCT_RATING_PRODUCT.PRODUCT_NAME} - {self.PRODUCT_RATING_VALUE}"

    @property
    def reviewer_name(self):
        if self.REVIEWER_NAME:
            return self.REVIEWER_NAME
        if self.PRODUCT_RATING_USER:
            return getattr(self.PRODUCT_RATING_USER, 'PUBLIC_USER_FULL_NAME', None) or getattr(self.PRODUCT_RATING_USER, 'FULL_NAME', None) or "Verified Client"
        return "Anonymous Customer"

    @property
    def reviewer_location(self):
        if self.REVIEWER_LOCATION:
            return self.REVIEWER_LOCATION
        if self.PRODUCT_RATING_USER:
            city = getattr(self.PRODUCT_RATING_USER, 'CITY', None)
            if city:
                return f"{city}, Nepal"
            addr = getattr(self.PRODUCT_RATING_USER, 'PUBLIC_USER_ADDRESS', '') or ''
            if addr:
                return addr.split(',')[0].strip() + ", Nepal"
        return "Nepal"

    @property
    def rating_stars(self):
        try:
            score = float(self.PRODUCT_RATING_VALUE)
            full = int(score)
            half = 1 if (score - full) >= 0.5 else 0
            empty = 5 - full - half
            return ("★" * full) + ("½" if half else "") + ("☆" * empty)
        except Exception:
            return "★★★★★"


#!--- PRODUCT ORDER MODEL -------
class ProductOrder(models.Model):
    PRODUCT_ORDER_ID = models.CharField(max_length=30, unique=True, editable=False)
    CUSTOMER = models.ForeignKey('users.PublicUserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="CUSTOMER_ORDERS")
    PRODUCT_ORDER_USER = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, null=True, blank=True, related_name="PRODUCT_ORDERS")
    PRODUCT_ORDER_PRODUCT = models.ForeignKey(ProductSetup, on_delete=models.PROTECT, null=True, blank=True, related_name="PRODUCT_ORDERS")
    PRODUCT_ORDER_QTY = models.DecimalField(max_digits=15, decimal_places=2, default=1.0)
    PRODUCT_ORDER_STATUS = models.CharField(max_length=30, choices=[
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ], default="PENDING")
    TOTAL_AMOUNT = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    SHIPPING_FEE = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    SHIPPING_NAME = models.CharField(max_length=255, blank=True, default="")
    SHIPPING_EMAIL = models.CharField(max_length=255, blank=True, default="")
    SHIPPING_PHONE = models.CharField(max_length=50, blank=True, default="")
    SHIPPING_ADDRESS = models.TextField(blank=True, default="")
    DELIVERY_INSTRUCTIONS = models.TextField(blank=True, default="")
    PAYMENT_METHOD = models.CharField(max_length=50, blank=True, default="COD")
    IS_PAID = models.BooleanField(default=False)
    ORDER_SOURCE = models.CharField(max_length=20, default="WEB", choices=[("WEB", "Customer Web Order"), ("INTERNAL", "Internal Order")])
    ORDER_ITEMS_DATA = models.JSONField(default=list, blank=True)
    PRODUCT_ORDER_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_ORDER_CREATED_BY")
    PRODUCT_ORDER_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_ORDER_MODIFIED_BY")
    PRODUCT_ORDER_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_ORDER_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT ORDER"

    def save(self, *args, **kwargs):
        if not self.PRODUCT_ORDER_ID:
            last_order = ProductOrder.objects.order_by("-id").first()
            next_id = (last_order.id + 1) if (last_order and last_order.id) else 1
            candidate = f"ORD-{next_id:06d}"
            while ProductOrder.objects.filter(PRODUCT_ORDER_ID=candidate).exists():
                next_id += 1
                candidate = f"ORD-{next_id:06d}"
            self.PRODUCT_ORDER_ID = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.PRODUCT_ORDER_ID

    @property
    def order_amount(self):
        if hasattr(self, '_order_amount') and self._order_amount is not None:
            return float(self._order_amount)
        if self.TOTAL_AMOUNT and float(self.TOTAL_AMOUNT) > 0:
            return float(self.TOTAL_AMOUNT)
        if self.PRODUCT_ORDER_PRODUCT and self.PRODUCT_ORDER_QTY:
            try:
                return float(self.PRODUCT_ORDER_QTY) * float(self.PRODUCT_ORDER_PRODUCT.PRODUCT_PRICE)
            except Exception:
                return 0.0
        return 0.0

    @order_amount.setter
    def order_amount(self, value):
        self._order_amount = value

    @property
    def customer_display_name(self):
        if self.SHIPPING_NAME:
            return self.SHIPPING_NAME
        if self.CUSTOMER and hasattr(self.CUSTOMER, 'PUBLIC_USER_FULL_NAME') and self.CUSTOMER.PUBLIC_USER_FULL_NAME:
            return self.CUSTOMER.PUBLIC_USER_FULL_NAME
        if self.PRODUCT_ORDER_USER and hasattr(self.PRODUCT_ORDER_USER, 'EMPLOYEE_FULL_NAME') and self.PRODUCT_ORDER_USER.EMPLOYEE_FULL_NAME:
            return self.PRODUCT_ORDER_USER.EMPLOYEE_FULL_NAME
        return "Customer"

    @property
    def product_display_name(self):
        if self.ORDER_ITEMS_DATA and len(self.ORDER_ITEMS_DATA) > 0:
            first_name = self.ORDER_ITEMS_DATA[0].get('name', 'Herbal Formulation')
            extra = len(self.ORDER_ITEMS_DATA) - 1
            return f"{first_name} (+{extra} more)" if extra > 0 else first_name
        if self.PRODUCT_ORDER_PRODUCT:
            return self.PRODUCT_ORDER_PRODUCT.PRODUCT_NAME
        return "Herbal Remedies"

    @property
    def items_count_or_qty(self):
        if self.ORDER_ITEMS_DATA:
            total_count = sum([int(it.get('quantity', 1)) for it in self.ORDER_ITEMS_DATA])
            if total_count > 0:
                return total_count
        return int(self.PRODUCT_ORDER_QTY) if self.PRODUCT_ORDER_QTY else 1



#!--- HOSPITAL & RESEARCH CENTER MODELS -------
class HospitalInfo(models.Model):
    HERO_BANNER_IMAGE = models.ImageField(upload_to="Uploads/Hospital/", blank=True, null=True)
    HERO_TITLE_ENG = models.CharField(max_length=255, blank=True, default="Holistic Hospital & Research Center")
    HERO_TITLE_NEP = models.CharField(max_length=255, blank=True, default="होलिस्टिक हस्पिटल एण्ड रिसर्च सेन्टर")
    HERO_SUBTITLE_ENG = models.CharField(max_length=500, blank=True, default="Integrated Natural Healthcare & Rehabilitation")
    HERO_SUBTITLE_NEP = models.CharField(max_length=500, blank=True, default="प्राकृतिक चिकित्सा र पुनस्र्थापना सेवा")

    INTRO_TITLE_ENG = models.CharField(max_length=255, blank=True, default="Introduction")
    INTRO_TITLE_NEP = models.CharField(max_length=255, blank=True, default="परिचय")
    INTRO_TEXT_NEP = models.TextField(help_text="Nepali intro paragraph from legacy website")
    INTRO_TEXT_ENG = models.TextField(blank=True, default="", help_text="English intro paragraph (falls back to Nepali)")

    DISEASES_TITLE_ENG = models.CharField(max_length=255, blank=True, default="Conditions & Diseases Treated")
    DISEASES_TITLE_NEP = models.CharField(max_length=255, blank=True, default="उपचार गरिने रोग तथा समस्याहरू")
    DISEASES_TEXT_NEP = models.TextField(help_text="Nepali disease list / descriptions from legacy website")
    DISEASES_TEXT_ENG = models.TextField(blank=True, default="", help_text="English disease list (falls back to Nepali)")

    PARALYSIS_TITLE_ENG = models.CharField(max_length=255, blank=True, default="Comprehensive Paralysis Rehabilitation")
    PARALYSIS_TITLE_NEP = models.CharField(max_length=255, blank=True, default="प्यारालाइसिस (पक्षघात) को सफल प्राकृतिक उपचार")
    PARALYSIS_DESC_NEP = models.TextField(blank=True, default="")
    PARALYSIS_DESC_ENG = models.TextField(blank=True, default="")
    PARALYSIS_BANNER_IMAGE = models.ImageField(upload_to="Uploads/Hospital/", blank=True, null=True)

    CONTACT_PHONE = models.CharField(max_length=100, blank=True, default="01-4115830, 9851088497")
    CONTACT_EMAIL = models.EmailField(blank=True, default="info@holisticnepal.com")
    CONTACT_LOCATION_ENG = models.CharField(max_length=255, blank=True, default="Thulo Kharibot Marga, Kathmandu, Bagmati Province 44600")
    CONTACT_LOCATION_NEP = models.CharField(max_length=255, blank=True, default="ठूलो खरीबोट मार्ग, काठमाडौं, बागमती प्रदेश ४४६००")

    IS_ACTIVE = models.BooleanField(default=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "HOSPITAL_INFO"
        verbose_name = "Hospital Information"
        verbose_name_plural = "Hospital Information"

    def __str__(self):
        return "Holistic Hospital & Research Center Info"

    @property
    def display_intro_eng(self):
        return self.INTRO_TEXT_ENG if self.INTRO_TEXT_ENG and self.INTRO_TEXT_ENG.strip() else self.INTRO_TEXT_NEP

    @property
    def display_intro_nep(self):
        return self.INTRO_TEXT_NEP if self.INTRO_TEXT_NEP and self.INTRO_TEXT_NEP.strip() else self.INTRO_TEXT_ENG

    @property
    def display_diseases_eng(self):
        return self.DISEASES_TEXT_ENG if self.DISEASES_TEXT_ENG and self.DISEASES_TEXT_ENG.strip() else self.DISEASES_TEXT_NEP

    @property
    def display_diseases_nep(self):
        return self.DISEASES_TEXT_NEP if self.DISEASES_TEXT_NEP and self.DISEASES_TEXT_NEP.strip() else self.DISEASES_TEXT_ENG

    @property
    def display_paralysis_eng(self):
        return self.PARALYSIS_DESC_ENG if self.PARALYSIS_DESC_ENG and self.PARALYSIS_DESC_ENG.strip() else self.PARALYSIS_DESC_NEP

    @property
    def display_paralysis_nep(self):
        return self.PARALYSIS_DESC_NEP if self.PARALYSIS_DESC_NEP and self.PARALYSIS_DESC_NEP.strip() else self.PARALYSIS_DESC_ENG


class HospitalService(models.Model):
    SERVICE_NAME_NEP = models.CharField(max_length=255)
    SERVICE_NAME_ENG = models.CharField(max_length=255, blank=True, default="")
    SERVICE_IMAGE = models.ImageField(upload_to="Uploads/Hospital/Services/", blank=True, null=True)
    SERVICE_ORDER = models.PositiveIntegerField(default=1)
    IS_ACTIVE = models.BooleanField(default=True)
    CREATED_AT = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "HOSPITAL_SERVICE"
        ordering = ["SERVICE_ORDER", "id"]
        verbose_name = "Hospital Service"
        verbose_name_plural = "Hospital Services"

    def __str__(self):
        return f"{self.SERVICE_ORDER}. {self.SERVICE_NAME_NEP} / {self.SERVICE_NAME_ENG or self.SERVICE_NAME_NEP}"

    @property
    def name_eng(self):
        return self.SERVICE_NAME_ENG if self.SERVICE_NAME_ENG and self.SERVICE_NAME_ENG.strip() else self.SERVICE_NAME_NEP

    @property
    def name_nep(self):
        return self.SERVICE_NAME_NEP if self.SERVICE_NAME_NEP and self.SERVICE_NAME_NEP.strip() else self.SERVICE_NAME_ENG


class HospitalServiceTag(models.Model):
    TAG_LABEL_NEP = models.CharField(max_length=255)
    TAG_LABEL_ENG = models.CharField(max_length=255, blank=True, default="")
    TAG_ORDER = models.PositiveIntegerField(default=1)
    IS_ACTIVE = models.BooleanField(default=True)

    class Meta:
        db_table = "HOSPITAL_SERVICE_TAG"
        ordering = ["TAG_ORDER", "id"]
        verbose_name = "Hospital Service Tag / Therapy"
        verbose_name_plural = "Hospital Service Tags / Therapies"

    def __str__(self):
        return f"{self.TAG_ORDER}. {self.TAG_LABEL_NEP} / {self.TAG_LABEL_ENG or self.TAG_LABEL_NEP}"

    @property
    def label_eng(self):
        return self.TAG_LABEL_ENG if self.TAG_LABEL_ENG and self.TAG_LABEL_ENG.strip() else self.TAG_LABEL_NEP

    @property
    def label_nep(self):
        return self.TAG_LABEL_NEP if self.TAG_LABEL_NEP and self.TAG_LABEL_NEP.strip() else self.TAG_LABEL_ENG


class Service(models.Model):
    slug = models.SlugField(unique=True, max_length=100, help_text="URL slug e.g. hydrotherapy")
    name_en = models.CharField(max_length=255)
    name_np = models.CharField(max_length=255)
    summary_en = models.CharField(max_length=500, help_text="One-line description in English")
    summary_np = models.CharField(max_length=500, help_text="One-line description in Nepali")
    hero_description_en = models.TextField(help_text="Full one-paragraph introduction in English")
    hero_description_np = models.TextField(help_text="Full one-paragraph introduction in Nepali")
    conditions_treated_en = models.JSONField(default=list, blank=True, help_text="List of strings in English")
    conditions_treated_np = models.JSONField(default=list, blank=True, help_text="List of strings in Nepali")
    how_it_works = models.JSONField(
        default=list,
        blank=True,
        help_text="List of step objects: [{'title_en': ..., 'title_np': ..., 'desc_en': ..., 'desc_np': ...}]"
    )
    duration = models.CharField(max_length=100, blank=True, default="45 Mins")
    physiological_action_en = models.CharField(max_length=255, blank=True, default="")
    physiological_action_np = models.CharField(max_length=255, blank=True, default="")
    primary_indication_en = models.CharField(max_length=255, blank=True, default="")
    primary_indication_np = models.CharField(max_length=255, blank=True, default="")
    icon = models.CharField(max_length=50, blank=True, default="leaf", help_text="Icon identifier e.g. droplet, leaf, hands")
    related_services = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='linked_from')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "HOSPITAL_SERVICE_PAGE"
        ordering = ['order', 'id']
        verbose_name = "Clinical Service Page"
        verbose_name_plural = "Clinical Service Pages"

    def __str__(self):
        return f"{self.order}. {self.name_en} / {self.name_np} ({self.slug})"

