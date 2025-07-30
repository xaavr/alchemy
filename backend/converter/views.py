from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MediaFile, ConversionJob
from .serializers import MediaFileSerializer, ConversionJobSerializer
from .tasks import convert_media_task

class MediaFileViewSet(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to upload

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MediaFile.objects.filter(user=self.request.user)
        
        # Important: Only return files if there is a session key
        session_id = self.request.session.session_key
        if session_id:
            return MediaFile.objects.filter(session_id=session_id, user__isnull=True)
        
        return MediaFile.objects.none() # Return an empty queryset if no session

    def perform_create(self, serializer):
        # Get the uploaded file object from the request
        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            # This case should be caught by serializer validation, but it's a good safeguard.
            return 

        # Prepare the data that needs to be set by the server
        extra_data = {
            'filename': uploaded_file.name,
            'filesize': uploaded_file.size,
        }

        # Associate with user or session
        if self.request.user.is_authenticated:
            extra_data['user'] = self.request.user
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            #     print(f"creating session...")
            # print(f"Session ID: {self.request.session.session_key}")
            extra_data['session_id'] = self.request.session.session_key
        
        # Save the instance, passing the extra data to be saved on the model
        serializer.save(**extra_data)

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
            print(f"Conversion job created for user: {self.request.user.username}")
        else:
            instance = serializer.save(session_id=self.request.session.session_key)
            print(f"Conversion job created for anonymous session: {self.request.session.session_key}")
        
        # Launch the background task with the new conversion's ID
        convert_media_task.delay(instance.id)

class InitSessionView(APIView):
    """
    Ensures a session is created and returns any existing files
    associated with that session in a single request.
    """
    def get(self, request, *args, **kwargs):
        # 1. Ensure a session exists.
        if not request.session.session_key:
            request.session.create()
            # 2. Explicitly save the session to the database immediately.
            request.session.save()

        # 3. Get the session key.
        session_key = request.session.session_key
        
        # 4. Find all files associated with this session.
        files = MediaFile.objects.filter(session_id=session_key)
        
        # 5. Serialize the file data.
        serializer = MediaFileSerializer(files, many=True)
        
        # 6. Return the list of files using DRF's Response.
        return Response(serializer.data)