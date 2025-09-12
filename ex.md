Here is the comprehensive project documentation.

New Files:

README.md

CONTRIBUTING.md

README.md
code
Markdown
download
content_copy
expand_less

# CTF Platform

A complete, feature-rich, and secure Capture The Flag (CTF) platform built with a modern technology stack. This project provides a full-featured backend API with Django and a reactive frontend with Vue.js, all containerized for easy deployment.

## Features

*   **User & Team Management:** Full support for user registration, profiles, and team creation/management.
*   **Flexible Scoring:** Supports both traditional **Static Scoring** (fixed points) and **Dynamic Scoring** where challenge values decrease with each solve.
*   **Real-time Activity Feed:** A live feed on the homepage broadcasts successful solves to all participants in real-time using WebSockets.
*   **Comprehensive Challenge Interaction:**
    *   Challenges with descriptions, tags, and downloadable files.
    *   Unlockable hints with point deductions.
    *   Rate-limited flag submission to prevent brute-forcing.
*   **Write-Up System:** Players can submit write-ups for solved challenges to earn bonus points, managed through an admin moderation queue.
*   **Live Leaderboard:** A real-time leaderboard ranks teams by score, using the earliest solve time as a tie-breaker.
*   **Admin Dashboard API:** A complete set of secure, admin-only API endpoints for managing users, teams, challenges, tags, and site content.
*   **Containerized & Deployable:** Comes with a full Docker Compose setup for easy local development and production deployment. Includes guides and manifests for deploying to Kubernetes.

## Technology Stack

| Component      | Technology                                                              |
|----------------|-------------------------------------------------------------------------|
| **Backend**    | Python, Django, Django REST Framework, Django Channels                  |
| **Frontend**   | Vue.js (v3), Pinia, Vue Router, Tailwind CSS, Axios                      |
| **Database**   | PostgreSQL                                                              |
| **Real-time**  | Redis, WebSockets (via Django Channels)                                 |
| **Deployment** | Docker, Docker Compose, Nginx, Daphne                                   |

## Prerequisites

To run this project, you will need the following installed on your local machine:
*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

## Local Development Setup

Follow these steps to get the entire platform running locally for development and testing.

1.  **Clone the Repository**
    ```sh
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create an Environment File**
    Create a file named `.env` in the project root. This file will hold all your configuration variables. Copy the contents of the example below into your `.env` file. For local development, these values are sufficient.

    **`.env` file contents:**
    ```env
    # Django Settings
    SECRET_KEY=your-super-secret-key-for-development
    DEBUG=1

    # Database Settings (for Docker Compose)
    POSTGRES_DB=ctf_db
    POSTGRES_USER=ctf_user
    POSTGRES_PASSWORD=ctf_pass

    # Redis Host (for Docker Compose)
    REDIS_HOST=redis
    ```

3.  **Build and Run the Containers**
    Use Docker Compose to build the images and start all the services (database, Redis, backend, frontend).
    ```sh
    docker-compose up --build
    ```
    The first build may take a few minutes.

4.  **Run Database Migrations**
    In a separate terminal, while the containers are running, execute the initial database migrations and create a superuser for the Django admin panel.
    ```sh
    # Apply database migrations
    docker-compose exec backend python manage.py migrate

    # Create an admin user
    docker-compose exec backend python manage.py createsuperuser
    ```

5.  **Access the Application**
    *   **Frontend:** The CTF platform will be available at `http://localhost:8080`.
    *   **Django Admin:** The backend admin panel is at `http://localhost:8080/admin/`.

## Configuration

The `docker-compose.yml` file is configured to read environment variables from the `.env` file at the project root.

| Variable              | Description                                                                 | Example Value                       |
|-----------------------|-----------------------------------------------------------------------------|-------------------------------------|
| `SECRET_KEY`          | A long, random string used for cryptographic signing in Django.             | `your-super-secret-key`             |
| `DEBUG`               | Toggles Django's debug mode. `1` for True, `0` for False.                   | `1`                                 |
| `POSTGRES_DB`         | The name of the PostgreSQL database.                                        | `ctf_db`                            |
| `POSTGRES_USER`       | The username for the PostgreSQL database.                                   | `ctf_user`                          |
| `POSTGRES_PASSWORD`   | The password for the PostgreSQL database user.                              | `ctf_pass`                          |
| `REDIS_HOST`          | The hostname of the Redis service for Django Channels.                      | `redis`                             |

## Production Deployment

### Using Docker Compose

For a small-scale production deployment, you can use the provided `docker-compose.yml` file with a few modifications to your `.env` file.

1.  **Set `DEBUG` to `0`** to turn off debugging mode.
2.  **Generate a strong `SECRET_KEY`**.
3.  **Configure `ALLOWED_HOSTS`** in `ctf_platform/settings.py` to include your domain name.

### Using Kubernetes (K8s)

For a scalable, robust deployment, Kubernetes is recommended. This requires a more advanced setup involving several key components:

*   **Deployment:** Manages the lifecycle of your application pods (e.g., backend, frontend).
*   **Service:** Provides a stable network endpoint to access your application pods.
*   **PersistentVolumeClaim (PVC):** Requests persistent storage for your database and any user-uploaded files (media).
*   **Ingress:** Manages external access to your services, handling HTTP/HTTPS routing.
*   **ConfigMap & Secret:** Externalizes configuration and securely stores sensitive data like passwords and API keys.

Below are simplified example manifests to guide your deployment.

#### Backend Deployment (`backend-deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-backend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ctf-backend
  template:
    metadata:
      labels:
        app: ctf-backend
    spec:
      containers:
      - name: backend
        image: your-registry/ctf-backend:latest # Replace with your image
        command: ["daphne", "-b", "0.0.0.0", "-p", "8000", "ctf_platform.asgi:application"]
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: ctf-config
        - secretRef:
            name: ctf-secret
```

#### Frontend Deployment & Service (`frontend-deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-frontend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ctf-frontend
  template:
    metadata:
      labels:
        app: ctf-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/ctf-frontend:latest # Replace with your image
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: ctf-frontend-service
spec:
  selector:
    app: ctf-frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

## Managing Dockerized Challenges

This platform is designed to support dynamic, containerized challenges. The intended workflow is as follows:

1.  **Challenge Creation:** An administrator creates a challenge in the admin dashboard.
2.  **Template Configuration:** In the challenge settings, the admin specifies the Docker image for the challenge (e.g., `your-registry/challenge-web-101:latest`).
3.  **Instance Launch:** When a player starts the challenge, the platform's backend signals a container orchestration service (like Kubernetes or a custom daemon).
4.  **Isolation & Access:** The service spins up a dedicated, isolated instance of the challenge container. The player is provided with the unique connection details (e.g., IP and port).
5.  **Resource Management:** The platform monitors the instance and automatically tears it down after a set period of inactivity to conserve resources.
```

### `CONTRIBUTING.md`
```markdown
# Contributing to the CTF Platform

Thank you for your interest in contributing! This document outlines the process and guidelines for developing on this project.

## Getting Started

For rapid development, you can run the backend and frontend services on your local machine without using Docker for every change.

### Backend (Django)

1.  **Set up a Python Virtual Environment:**
    ```sh
    # Navigate to the backend directory
    cd ctf_platform

    # Create and activate a virtual environment
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Run Local Services:**
    You will need a local instance of PostgreSQL and Redis running. You can install them directly or use Docker for convenience:
    ```sh
    docker run --name local-postgres -e POSTGRES_PASSWORD=ctf_pass -e POSTGRES_USER=ctf_user -e POSTGRES_DB=ctf_db -p 5432:5432 -d postgres:15-alpine
    docker run --name local-redis -p 6379:6379 -d redis:7-alpine
    ```

4.  **Run the Development Server:**
    Ensure your `ctf_platform/settings.py` is pointed to your local database (`localhost`). Then, run the server:
    ```sh
    python manage.py runserver
    ```

### Frontend (Vue.js)

1.  **Navigate to the Frontend Directory:**
    ```sh
    cd frontend
    ```

2.  **Install NPM Dependencies:**
    ```sh
    npm install
    ```

3.  **Run the Vite Development Server:**
    This will start a hot-reloading development server, typically on `http://localhost:5173`.
    ```sh
    npm run serve
    ```
    Ensure you update the `baseURL` in `frontend/src/services/api.js` to point to your local Django server (`http://127.0.0.1:8000`).

## Code Style

*   **Python/Django:** Please adhere to **PEP 8** style guidelines. We recommend using an autoformatter like `black` to ensure consistency.
*   **Vue.js/JavaScript:** We use **Prettier** for code formatting. Please format your code before committing.

## Backend Development

### Database Migrations

If you make changes to the Django models (`api/models.py`), you must create a new migration file and apply it.

1.  **Create Migrations:**
    ```sh
    python ctf_platform/manage.py makemigrations
    ```

2.  **Apply Migrations:**
    ```sh
    python ctf_platform/manage.py migrate
    ```

### Running Tests

To ensure code quality and prevent regressions, please run the test suite after making changes.

```sh
python ctf_platform/manage.py test
```

## Commit & Pull Request Process

1.  **Create a Feature Branch:**
    Branch off of the `main` or `develop` branch for your new feature or bugfix.
    ```sh
    git checkout -b feature/my-new-feature
    ```

2.  **Make Your Changes:**
    Implement your changes and commit them with clear, descriptive messages.

3.  **Push Your Branch:**
    ```sh
    git push origin feature/my-new-feature
    ```

4.  **Open a Pull Request:**
    Go to the repository on GitHub and open a Pull Request. Provide a clear title and a detailed description of the changes you've made. Link to any relevant issues.
```
