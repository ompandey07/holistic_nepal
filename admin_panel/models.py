from users.models import EmployeeSetup
from django.utils import timezone
from django.db import models


#!--- GALLERY MODEL -------
class Gallery(models.Model):
    GALLERY_TITLE = models.CharField(max_length=500)
    GALLERY_IMAGE = models.ImageField(upload_to="Uploads/Gallary/")
    GALLERY_DESCRIPTION = models.TextField()
    GALLERY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_CREATED_BY")
    GALLERY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="GALLERY_MODIFIED_BY")
    GALLERY_CREATED_AT = models.DateTimeField(default=timezone.now)
    GALLERY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GALLERY"

    def __str__(self):
        return self.GALLERY_TITLE


# !--- NEWS MODEL -------
class News(models.Model):
    NEWS_TYPE = models.CharField(max_length=50, choices=[
        ("GENERAL", "General"),
        ("ANNOUNCEMENT", "Announcement"),
        ("EVENT", "Event"),
        ("UPDATE", "Update"),
        ("NOTICE", "Notice"),
        ("BLOG", "Blog"),
        ("PRESS_RELEASE", "Press Release"),
    ])
    NEWS_TITLE = models.CharField(max_length=500)
    NEWS_IMAGE = models.ImageField(upload_to="Uploads/News/")
    NEWS_DESCRIPTION = models.TextField()
    NEWS_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="NEWS_CREATED_BY")
    NEWS_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="NEWS_MODIFIED_BY")
    NEWS_CREATED_AT = models.DateTimeField(default=timezone.now)
    NEWS_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "NEWS"

    def __str__(self):
        return self.NEWS_TITLE


#!--- UNIT SETUP MODEL -------
class UnitSetup(models.Model):
    UNIT_NAME = models.CharField(max_length=200)
    UNIT_SYMBOL = models.CharField(max_length=50)
    UNIT_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="UNIT_CREATED_BY")
    UNIT_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="UNIT_MODIFIED_BY")
    UNIT_CREATED_AT = models.DateTimeField(default=timezone.now)
    UNIT_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UNIT SETUP"

    def __str__(self):
        return self.UNIT_NAME


#!--- PRODUCT CATEGORY MODEL -------
class ProductCategory(models.Model):
    CATEGORY_NAME = models.CharField(max_length=200)
    CATEGORY_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="CATEGORY_CREATED_BY")
    CATEGORY_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="CATEGORY_MODIFIED_BY")
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
    PRODUCT_RATING = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    PRODUCT_DESCRIPTION = models.TextField()
    PRODUCT_IMAGE = models.ImageField(upload_to="Uploads/Product Images/")
    PRODUCT_CREATED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="PRODUCT_CREATED_BY")
    PRODUCT_MODIFIED_BY = models.ForeignKey(EmployeeSetup, on_delete=models.PROTECT, related_name="PRODUCT_MODIFIED_BY")
    PRODUCT_CREATED_AT = models.DateTimeField(default=timezone.now)
    PRODUCT_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PRODUCT SETUP"

    def __str__(self):
        return self.PRODUCT_NAME


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