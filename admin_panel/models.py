from users.models import UserProfile
from django.utils import timezone
from django.db import models



class Gallery(models.Model):
    GALLERY_TITLE = models.CharField(max_length=500)
    GALLERY_IMAGE = models.ImageField(upload_to="Uploads/Gallary/")
    GALLERY_DESCRIPTION = models.TextField()
    GALLERY_CREATED_BY = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="GALLERY_CREATED_BY")
    GALLERY_MODIFIED_BY = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="GALLERY_MODIFIED_BY")
    GALLERY_CREATED_AT = models.DateTimeField(default=timezone.now)
    GALLERY_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GALLERY"

    def __str__(self):
        return self.GALLERY_TITLE