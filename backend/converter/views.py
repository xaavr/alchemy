from rest_framework import viewsets, permissions
from .models import MediaFile, ConversionJob
from .serializers import MediaFileSerializer, ConversionJobSerializer

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversionJobViewSet(viewsets.ModelViewSet):
    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobSerializer
    permission_classes = [permissions.IsAuthenticated]
