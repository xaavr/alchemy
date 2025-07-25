from django.test import TestCase

# Create your tests here.
# Step 1: (Optional) Get an auth token if you want to test as a logged-in user
# Replace 'your_username' and 'your_password'
# TOKEN=$(curl -s -X POST -d "username=your_username&password=your_password" http://localhost:8000/api-token-auth/ | cut -d'"' -f4)
# echo "Auth Token: $TOKE"N

# Step 2: Upload a file (e.g., a file named 'test.mp4')
# If using a token, add: -H "Authorization: Token $TOKEN"
# FILE_RESPONSE=$(curl -s -X POST -H "Authorization: Token $TOKEN" -F "file=@/path/to/your/test.mp4" http://localhost:8000/api/files/)
# echo "File Upload Response: $FILE_RESPONSE"

# Extract the file ID from the response
# FILE_ID=$(echo $FILE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
# echo "Uploaded File ID: $FILE_ID"

# Step 3: Request a conversion to 'mkv'
# If using a token, add: -H "Authorization: Token $TOKEN"
# CONVERSION_RESPONSE=$(curl -s -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" -d "{\"original_file\": \"$FILE_ID\", \"target_format\": \"mkv\"}" http://localhost:8000/api/conversions/)
# echo "Conversion Response: $CONVERSION_RESPONSE"

# Step 4: Check the logs of your celery worker to see the task run
# docker-compose logs -f celery

# Upload the file and save the session cookie
# FILE_RESPONSE=$(curl -s -c cookies.txt -F "file=@test.mp4" http://localhost:8000/api/files/)
# echo "File Upload Response: $FILE_RESPONSE"