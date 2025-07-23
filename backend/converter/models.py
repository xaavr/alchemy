import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    filesize = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.user.username})"
    
class ConversionJob(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversions')
    original_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name='conversions')
    converted_file = models.FileField(upload_to='converted/', null=True, blank=True)
    target_format = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conversion {self.id} for {self.original_file.filename}"