from django.utils import timezone
from django.db import models



#!- -- PUBLIC USER PROFILE MODEL ------- 
class PublicUserProfile(models.Model):
    PUBLIC_USER_FULL_NAME = models.CharField(max_length=200)
    PUBLIC_USER_EMAIL = models.EmailField()
    PUBLIC_USER_MOBILE_NO = models.CharField(max_length=15)
    PUBLIC_USER_ADDRESS = models.TextField()
    PUBLIC_USER_IP = models.CharField(max_length=45)
    PUBLIC_USER_PASSWORD = models.CharField(max_length=255)
    PUBLIC_USER_PROFILE_IMAGE = models.ImageField(upload_to="Uploads/Public/Profile_Images/", null=True, blank=True)
    PUBLIC_USER_CREATED_BY = models.CharField(max_length=200, null=True, blank=True)
    PUBLIC_USER_MODIFIED_BY = models.CharField(max_length=200, null=True, blank=True)
    PUBLIC_USER_CREATED_AT = models.DateTimeField(default=timezone.now)
    PUBLIC_USER_UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "PUBLIC USER PROFILE"
        verbose_name = "Public User Profile"
        verbose_name_plural = "Public User Profiles"

    def __str__(self):
        return self.PUBLIC_USER_FULL_NAME


#!--- EMPLOYEE SETUP MODEL ------- 
class EmployeeSetup(models.Model):
    ROLE_CHOICES = [("ADMIN", "Admin"), ("CASHIER", "Cashier"), ("DELIVERY_MAN", "Delivery Man"), ("MANAGER", "Manager"), ("STAFF", "Staff")]
    EMPLOYEE_FULL_NAME = models.CharField(max_length=200)
    EMPLOYEE_EMAIL = models.EmailField()
    EMPLOYEE_MOBILE_NO = models.CharField(max_length=15, null=True, blank=True)
    EMPLOYEE_ADDRESS = models.TextField()
    EMPLOYEE_IP = models.CharField(max_length=45, null=True, blank=True)
    EMPLOYEE_ROLE = models.CharField(max_length=20, choices=ROLE_CHOICES, default="STAFF")
    EMPLOYEE_PASSWORD = models.CharField(max_length=255)
    EMPLOYEE_CREATED_BY = models.CharField(max_length=200, null=True, blank=True)
    EMPLOYEE_MODIFIED_BY = models.CharField(max_length=200, null=True, blank=True)
    EMPLOYEE_CREATED_AT = models.DateTimeField(default=timezone.now)
    EMPLOYEE_UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "EMPLOYEE SETUP"
        verbose_name = "Employee Setup"
        verbose_name_plural = "Employee Setups"

    def __str__(self):
        return self.EMPLOYEE_FULL_NAME