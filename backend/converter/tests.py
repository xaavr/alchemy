from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import MediaFile, ConversionJob
from rest_framework import status
import os

# Your curl commands can be removed or kept for reference
# curl -v -c cookies.txt -F "file=@test.jpg" http://localhost:8000/api/files/
# CSRF_TOKEN=$(grep 'csrftoken' cookies.txt | cut -f7) && curl -v -b cookies.txt -X POST -H "Content-Type: application/json" -H "X-CSRFToken: $CSRF_TOKEN" -d '{"original_file_id": "<PASTE_THE_FILE_ID_HERE>", "target_format": "png"}' http://localhost:8000/api/conversions/

class ConversionAPITestCase(APITestCase):
    def test_upload_and_convert_flow(self):
        """
        Tests the full anonymous workflow:
        1. Upload a file.
        2. Request a conversion for that file.
        """
        # 1. Upload a file
        # Create a simple dummy file in memory
        dummy_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        upload_url = '/api/files/'
        upload_response = self.client.post(upload_url, {'file': dummy_file}, format='multipart')

        # Check that the upload was successful
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', upload_response.data)
        
        # Get the ID of the uploaded file
        file_id = upload_response.data['id']
        self.assertEqual(MediaFile.objects.count(), 1)

        # 2. Request a conversion
        conversion_url = '/api/conversions/'
        conversion_data = {
            'original_file_id': file_id,
            'target_format': 'png'
        }
        
        conversion_response = self.client.post(conversion_url, conversion_data, format='json')

        # Check that the conversion job was created successfully
        self.assertEqual(conversion_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConversionJob.objects.count(), 1)
        
        # Verify the created job has the correct details
        conversion_job = ConversionJob.objects.first()
        self.assertEqual(str(conversion_job.original_file.id), file_id)
        self.assertEqual(conversion_job.target_format, 'png')
        self.assertEqual(conversion_job.status, 'PENDING')