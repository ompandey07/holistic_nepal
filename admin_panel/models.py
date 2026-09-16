from users.models import EmployeeSetup , PublicUserProfile
from django.utils import timezone
from django.db import models
from django.utils.text import slugify


#!--- GALLERY MODEL -------
class Gallery(models.Model):
    GALLERY_TITLE = models.CharField(max_length=500)
    GALLERY_SLUG = models.SlugField(max_length=500, unique=True, blank=True)
    GALLERY_IMAGE = models.ImageField(upload_to="Uploads/Gallary/")
    GALLERY_DESCRIPTION = models.TextField()
    GALLERY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_CREATED_BY")
    GALLERY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_MODIFIED_BY")
    GALLERY_CREATED_AT = models.DateTimeField(default=timezone.now)
    GALLERY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GALLERY"

    def save(self, *args, **kwargs):
        if not self.GALLERY_SLUG:
            self.GALLERY_SLUG = slugify(self.GALLERY_TITLE)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.GALLERY_TITLE


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
    NEWS_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="NEWS_CREATED_BY")
    NEWS_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="NEWS_MODIFIED_BY")
    NEWS_CREATED_AT = models.DateTimeField(default=timezone.now)
    NEWS_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "NEWS"

    def save(self, *args, **kwargs):
        if not self.NEWS_SLUG:
            self.NEWS_SLUG = slugify(self.NEWS_TITLE)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.NEWS_TITLE


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
    CATEGORY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="CATEGORY_CREATED_BY")
    CATEGORY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="CATEGORY_MODIFIED_BY")
    CATEGORY_CREATED_AT = models.DateTimeField(default=timezone.now)
    CATEGORY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT CATEGORY"

    def __str__(self):
        return self.CATEGORY_NAME


# !--- PRODUCT SETUP MODEL -------
class ProductSetup(models.Model):
    PRODUCT_NAME = models.CharField(max_length=300)
    PRODUCT_UNIT = models.ForeignKey(UnitSetup, on_delete=models.PROTECT, related_name="PRODUCT_UNIT")
    PRODUCT_CATEGORY = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="PRODUCT_CATEGORY")
    PRODUCT_PRICE = models.DecimalField(max_digits=15, decimal_places=2)
    PRODUCT_DESCRIPTION = models.TextField()
    PRODUCT_IMAGE = models.ImageField(upload_to="Uploads/Product Images/")
    PRODUCT_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_CREATED_BY")
    PRODUCT_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.SET_NULL, null=True, blank=True, related_name="PRODUCT_MODIFIED_BY")
    PRODUCT_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT SETUP"

    def __str__(self):
        return self.PRODUCT_NAME

    @property
    def slug(self):
        return slugify(self.PRODUCT_NAME)


# !--- PRODUCT RATING MODEL -------
class ProductRating(models.Model):
    PRODUCT_RATING_PRODUCT = models.ForeignKey(ProductSetup, on_delete=models.CASCADE, related_name="PRODUCT_RATINGS")
    PRODUCT_RATING_USER = models.ForeignKey(PublicUserProfile, on_delete=models.CASCADE, related_name="PRODUCT_RATINGS")
    PRODUCT_RATING_VALUE = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    PRODUCT_RATING_COMMENT = models.TextField(null=True, blank=True)
    PRODUCT_RATING_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_RATING_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT RATING"

    def __str__(self):
        return f"{self.PRODUCT_RATING_PRODUCT.PRODUCT_NAME} - {self.PRODUCT_RATING_VALUE}"


#!--- PRODUCT ORDER MODEL -------
class ProductOrder(models.Model):
    PRODUCT_ORDER_ID = models.CharField(max_length=30, unique=True, editable=False)
    PRODUCT_ORDER_USER = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="PRODUCT_ORDERS")
    PRODUCT_ORDER_PRODUCT = models.ForeignKey(ProductSetup, on_delete=models.PROTECT, related_name="PRODUCT_ORDERS")
    PRODUCT_ORDER_QTY = models.DecimalField(max_digits=15, decimal_places=2)
    PRODUCT_ORDER_STATUS = models.CharField(max_length=30, choices=[
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ], default="PENDING")
    PRODUCT_ORDER_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="PRODUCT_ORDER_CREATED_BY")
    PRODUCT_ORDER_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="PRODUCT_ORDER_MODIFIED_BY")
    PRODUCT_ORDER_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_ORDER_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT ORDER"

    def save(self, *args, **kwargs):
        if not self.PRODUCT_ORDER_ID:
            last_order = ProductOrder.objects.order_by("-id").first()
            next_id = (last_order.id + 1) if last_order else 1
            self.PRODUCT_ORDER_ID = f"ORD-{next_id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.PRODUCT_ORDER_ID