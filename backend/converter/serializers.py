from rest_framework import serializers
from .models import MediaFile, ConversionJob

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'filename', 'file', 'filesize', 'uploaded_at', 'user']

class ConversionJobSerializer(serializers.ModelSerializer):
    original_file = MediaFileSerializer(read_only=True)

    class Meta:
        model = ConversionJob
        fields = [
            'id',
            'original_file',
            'target_format',
            'status',
            'result_file',
            'created_at',
            'completed_at',
            'error_message',
            'is_public',
        ]
