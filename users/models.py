from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    USER_FULL_NAME = models.CharField(max_length=200)
    USER_EMAIL = models.EmailField()
    USER_MOBILE_NO = models.CharField(max_length=15)
    USER_ADDRESS = models.TextField()
    USER_IP = models.CharField(max_length=45)

    USER_CREATED_BY = models.CharField(max_length=200, null=True, blank=True)
    USER_MODIFIED_BY = models.CharField(max_length=200, null=True, blank=True)

    USER_CREATED_AT = models.DateTimeField(default=timezone.now)
    USER_UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "USER PROFILE"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.USER_FULL_NAME
    