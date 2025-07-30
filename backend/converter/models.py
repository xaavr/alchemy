import uuid
import os
from django.conf import settings
from django.db import models

def user_directory_path(instance, filename):
    """
    Generates a unique path for an uploaded or converted file.
    - Original uploads go to: uploads/user_<id>/<uuid>.<ext>
    - Converted files go to:  converted/user_<id>/<uuid>.<ext>
    """
    # Determine the base directory based on the model instance type
    if instance.__class__.__name__ == 'MediaFile':
        base_dir = 'uploads'
    else: # Assumes ConversionJob
        base_dir = 'converted'

    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4()}{ext}"
    
    # Determine the subdirectory based on user or session
    if instance.user:
        subdir = f"user_{instance.user.id}"
    else:
        # Use the first 8 characters of the session ID for a cleaner path
        subdir = f"session_{instance.session_id[:8]}"
        
    return os.path.join(base_dir, subdir, unique_filename)

    
class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # User can be null for anonymous uploads
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_files', null=True, blank=True)
    # Session ID for tracking anonymous users
    session_id = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    file = models.FileField(upload_to=user_directory_path)
    filename = models.CharField(max_length=255)
    filesize = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{self.filename} ({user_info})"
    

class ConversionJob(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversions', null=True, blank=True)
    session_id = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    original_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name='conversions')
    converted_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    target_format = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    task_id = models.CharField(max_length=255, null=True, blank=True, help_text="Celery task ID")
    error_message = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conversion {self.id} for {self.original_file.filename}"