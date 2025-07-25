from rest_framework import viewsets, permissions
from .models import MediaFile, ConversionJob
from .serializers import MediaFileSerializer, ConversionJobSerializer
from .tasks import convert_media_task

class MediaFileViewSet(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    # Allow any user, authenticated or not
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Returns files for the currently authenticated user,
        or for the current anonymous session.
        """
        if self.request.user.is_authenticated:
            return MediaFile.objects.filter(user=self.request.user)
        
        # For anonymous users, filter by session_id from the session
        session_id = self.request.session.session_key
        if not session_id:
            return MediaFile.objects.none() # No session, no files
        return MediaFile.objects.filter(session_id=session_id, user__isnull=True)

    def perform_create(self, serializer):
        """
        Saves the file, associating it with a user if authenticated,
        or with a session ID if anonymous.
        """
        uploaded_file = self.request.data.get('file')
        
        # Ensure the session exists
        if not self.request.session.session_key:
            self.request.session.create()

        if self.request.user.is_authenticated:
            serializer.save(
                user=self.request.user,
                filename=uploaded_file.name,
                filesize=uploaded_file.size
            )
        else:
            serializer.save(
                session_id=self.request.session.session_key,
                filename=uploaded_file.name,
                filesize=uploaded_file.size
            )

class ConversionJobViewSet(viewsets.ModelViewSet):
    serializer_class = ConversionJobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Returns conversions for the currently authenticated user,
        or for the current anonymous session.
        """
        if self.request.user.is_authenticated:
            return ConversionJob.objects.filter(user=self.request.user)
        
        session_id = self.request.session.session_key
        if not session_id:
            return ConversionJob.objects.none()
        return ConversionJob.objects.filter(session_id=session_id, user__isnull=True)
    
    def perform_create(self, serializer):
        """
        Saves the conversion, associating with user or session,
        and then launches the background conversion task.
        """
        if not self.request.session.session_key:
            self.request.session.create()

        # Save the instance first to get an ID
        if self.request.user.is_authenticated:
            instance = serializer.save(user=self.request.user)
        else:
            instance = serializer.save(session_id=self.request.session.session_key)
        
        # Launch the background task with the new conversion's ID
        convert_media_task.delay(instance.id)