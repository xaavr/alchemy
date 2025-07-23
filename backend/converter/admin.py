from django.contrib import admin
from .models import ConversionJob, MediaFile

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'filesize', 'uploaded_at')

@admin.register(ConversionJob)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ('original_file', 'target_format', 'status', 'created_at', 'completed_at')