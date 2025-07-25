# Alchemy File Conversion Service

Alchemy is a cloud-native file conversion service built with Django and React. It provides a platform for users to upload media files, convert them to various formats using FFmpeg, and manage their conversion history.

## Core Features

*   **File Upload:** Users can upload media files through a RESTful API.
*   **Asynchronous Conversion:** File conversions are handled asynchronously using Celery and Redis, ensuring the application remains responsive.
*   **FFmpeg Integration:** Leverages the power of FFmpeg for robust and high-quality media format conversions.
*   **Containerized Services:** The entire stack (Django, PostgreSQL, Redis) is containerized with Docker for consistent development and deployment environments.

### Planned Features

*   **User Authentication:** Secure user accounts with storage quotas for a free tier.
*   **Google Cloud Storage (GCS) Integration:** Store and serve all media files directly from GCS.
*   **React Frontend:** A modern, responsive user interface for uploading files and tracking conversion status.
*   **Public/Private Sharing:** Allow users to share links to their converted files.
*   **Deployment to Google Cloud:** Scalable deployment using Cloud Run or GKE.

## Technology Stack

*   **Backend:** Django, Django REST Framework
*   **Frontend (Planned):** React
*   **Async Task Queue:** Celery
*   **Message Broker/Cache:** Redis
*   **Database:** PostgreSQL
*   **Containerization:** Docker, Docker Compose
*   **Target Cloud Platform:** Google Cloud (GCS, Cloud Run, Cloud SQL)

## Getting Started

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd alchemy
    ```

2.  **Environment Variables:**
    Create a `.env` file in the root directory by copying the `.env.example` (if available). This file will store secrets and environment-specific configurations.

3.  **Build and Run with Docker:**
    ```sh
    docker-compose up --build
    ```

4.  **Apply Database Migrations:**
    In a separate terminal, run the initial Django migrations:
    ```sh
    docker-compose exec backend python manage.py migrate
    ```

The application should now be running and