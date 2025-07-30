from rest_framework import serializers
from .models import MediaFile, ConversionJob

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'filename', 'filesize', 'uploaded_at', 'user', 'session_id']
        read_only_fields = ('filename', 'filesize', 'uploaded_at', 'user', 'session_id')
        extra_kwargs = {
            # 'file' is for upload only. It's required but not sent back in the response.
            'file': {'write_only': True, 'required': True}
        }

class ConversionJobSerializer(serializers.ModelSerializer):
    # This field is for accepting the ID on creation/update
    original_file_id = serializers.PrimaryKeyRelatedField(
        queryset=MediaFile.objects.all(), source='original_file', write_only=True
    )
    # This field is for displaying the nested object on retrieval
    original_file = MediaFileSerializer(read_only=True)

    class Meta:
        model = ConversionJob
        fields = [
            'id',
            'original_file',
            'original_file_id', # Add the write-only field
            'target_format',
            'status',
            'converted_file',
            'created_at',
            'completed_at',
            'error_message',
            'is_public',
            'task_id', # Add the task_id field
        ]
        read_only_fields = ('status', 'converted_file', 'created_at', 'completed_at', 'error_message', 'task_id')
