import os
import subprocess
from celery import shared_task
from django.conf import settings
from .models import ConversionJob
from django.utils import timezone
from django.core.files.base import File

@shared_task(bind=True)
def convert_media_task(self, conversion_id):
    try:
        conversion = ConversionJob.objects.select_related('original_file').get(id=conversion_id)
        
        # Update status and save the Celery task ID
        conversion.status = ConversionJob.Status.PROCESSING
        conversion.task_id = self.request.id
        conversion.save()

        input_path = conversion.original_file.file.path
        original_basename = os.path.splitext(os.path.basename(conversion.original_file.filename))[0]
        output_format = conversion.target_format
        
        # This will be the filename passed to the user_directory_path function
        output_filename = f"{original_basename}.{output_format}"

        # Get the FileField instance from the model
        field = conversion._meta.get_field('converted_file')
        
        # Let Django's storage system generate the full, unique path
        # This calls your `user_directory_path` function internally
        full_output_path = field.storage.path(field.generate_filename(conversion, output_filename))
        
        # Get the directory part of the full path
        output_dir = os.path.dirname(full_output_path)
        
        # Ensure the output directory (e.g., media/converted/user_123/) exists
        os.makedirs(output_dir, exist_ok=True)

        # Choose the correct conversion tool based on the input file format
        if input_path.lower().endswith('.heic'):
            command = [
                'convert', # Use ImageMagick's convert tool
                input_path,
                full_output_path
            ]
        else:
            # Fallback to ffmpeg for other formats
            command = [
                'ffmpeg',
                '-i', input_path,
                full_output_path
            ]
        
        # Run the conversion command
        subprocess.run(command, check=True, capture_output=True, text=True)

        # The file is already in place, so just update the model field with the path
        # Django's storage backend knows MEDIA_ROOT, so we just need the relative path
        relative_path = os.path.relpath(full_output_path, settings.MEDIA_ROOT)
        conversion.converted_file.name = relative_path
        conversion.status = ConversionJob.Status.COMPLETED
        conversion.completed_at = timezone.now()
        conversion.save()

    except Exception as e:
        conversion.status = ConversionJob.Status.FAILED
        # Save the error message for debugging
        conversion.error_message = str(e) 
        conversion.save()
        raise
