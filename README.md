- `README.md`
- `CONTRIBUTING.md`

```markdown
# README.md
# CTF Platform

## Introduction
The CTF Platform is a comprehensive Capture The Flag (CTF) competition system designed to host, manage, and facilitate cybersecurity challenges for individuals and teams. It provides a robust backend API, a dynamic frontend interface, and administrative tools to run engaging CTF events.

## Features

### Frontend (User-Facing) Interface (Vue.js)
*   **Navigation Bar:**
    *   Clickable logo returning to the homepage.
    *   Links for "Challenges," "Leaderboard," "Teams," and "Rules/FAQ."
    *   User Controls: Profile link (with picture/score), Notifications icon, and Logout/Login buttons.
*   **Core Pages & Features:**
    *   **Homepage:** Customizable landing page with editable banner, welcome message, and event countdown. Includes a live activity feed.
    *   **Challenge Pages:**
        *   **List View:** Displays all challenges, filterable by editable tags/categories, points, and solved status.
        *   **Challenge Details:** Individual page with description, file downloads, hint requests, and flag submission form.
    *   **Leaderboard:** Real-time scoreboard for players and teams.
    *   **Teams:** Pages for team creation, management, and viewing rosters.
    *   **User Profiles:** Public profiles showing solved challenges, achievements, and team affiliation.
    *   **Live Activity Feed:** Real-time feed on the dashboard showing recent flag submissions via WebSockets.
*   **Gameplay & Scoring:**
    *   **Scoring System:** Supports both Static (fixed points) and Dynamic (points decrease with solves) models.
    *   **Bonus Points:** Configurable bonus points for "First Blood" and other achievements.
    *   **Trophies/Badges:** An achievement system to reward players (future implementation).
    *   **Write-up Submission:** Allows users to submit write-ups for bonus points, including an admin moderation queue and a public archive.

### Admin Dashboard (Backend Interface)
*   **Dashboard:** Overview of key analytics (active users, challenge status).
*   **General Settings:** Master panel for controlling global game state, UI elements, and scoring mode (static/dynamic).
*   **CTF Event Settings:** Controls for start/end times and scheduled challenge releases (future implementation).
*   **User Management:** Tables to view, search, filter, and manage users and teams, including mass management tools and user verification toggles.
*   **Challenge Management:** Create, view, and edit challenges; manage challenge types, tags, and dependencies.
*   **Dynamic Challenge Management:** Resource monitoring for running instances and managing challenge templates (future implementation).
*   **Content Management:** WYSIWYG editor for rich-text content (rules, FAQs, homepage).
*   **Write-up Moderation:** Queue for reviewing and approving submissions.
*   **Logs & Analytics:** Audit log viewer and detailed reports on submissions, challenges, and player engagement (future implementation).
*   **Infrastructure:** Dashboard for monitoring server health and database status (future implementation).

## Technology Stack

### Frontend
*   **Framework:** Vue.js (v3)
*   **State Management:** Pinia
*   **Routing:** Vue Router
*   **Styling:** Tailwind CSS
*   **HTTP Client:** Axios
*   **WebSocket Client:** Reconnecting-Websocket

### Backend
*   **Framework:** Python with Django
*   **API:** Django Rest Framework
*   **Database:** PostgreSQL
*   **Real-time:** Django Channels with Redis as channel layer
*   **Authentication:** OAuth 2.0 (via JWT - Simple JWT)
*   **Password Hashing:** Argon2 or Bcrypt (handled by Django's default if `argon2-cffi` or `bcrypt` are installed and configured)
*   **Rate Limiting:** `django-ratelimit`
*   **WYSIWYG Editor:** TinyMCE or Quill (for rich-text content, integrated on frontend consuming content API)

### Infrastructure
*   **Containerization:** Docker
*   **Orchestration:** Kubernetes (K8s)
*   **Web Server:** Nginx (for frontend and proxying)

## Prerequisites

To run this project locally using Docker, you need:

*   **Git:** For cloning the repository.
*   **Docker Desktop:** Includes Docker Engine and Docker Compose.
    *   [Install Docker Desktop](https://www.docker.com/products/docker-desktop)

## Local Development Setup

Follow these steps to get the CTF platform running on your local machine using Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ctf-platform.git
    cd ctf-platform
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the project root directory (same level as `docker-compose.yml`) and populate it with the required environment variables. Refer to the [Configuration](#configuration) section for details.
    ```env
    # .env example
    DJANGO_SECRET_KEY='your_super_secret_key_here'
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
    CORS_ALLOWED_ORIGINS='http://localhost:8080' # Vue dev server

    POSTGRES_DB=ctf_db
    POSTGRES_USER=ctf_user
    POSTGRES_PASSWORD=ctf_pass
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    REDIS_URL=redis://redis:6379/1
    ```

3.  **Build and run the Docker containers:**
    This command will build the `backend` and `frontend` images (if not already built or if changes detected) and start all services defined in `docker-compose.yml` in detached mode.
    ```bash
    docker-compose up --build -d
    ```

4.  **Run database migrations:**
    The `backend` service automatically runs migrations on startup as part of its `command` in `docker-compose.yml`. You can verify logs if needed.

5.  **Create a Django superuser (for admin access):**
    You'll need a superuser to access the Django admin panel and the custom admin API endpoints.
    ```bash
    docker exec -it ctf-platform-backend-1 python manage.py createsuperuser
    # Follow the prompts to create your superuser.
    ```
    *(Note: `ctf-platform-backend-1` is the default container name. Adjust if yours differs, e.g., by running `docker ps` to find the correct name.)*

6.  **Access the application:**
    *   **Frontend (Vue.js):** Open your browser and navigate to `http://localhost:8080`.
    *   **Django Admin:** Open your browser and navigate to `http://localhost:8080/admin/`.
    *   **Backend API Root:** `http://localhost:8080/api/`

## Configuration

The `.env` file is crucial for configuring the application.

| Variable              | Description                                                                                             | Example Value                  |
| :-------------------- | :------------------------------------------------------------------------------------------------------ | :----------------------------- |
| `DJANGO_SECRET_KEY`   | **CRITICAL:** A long, random string. Used for cryptographic signing. **Never expose in public.**       | `'your_super_secret_key_here'` |
| `DJANGO_DEBUG`        | Set to `True` for development, `False` for production. Affects error reporting and static file serving. | `True`                         |
| `DJANGO_ALLOWED_HOSTS`| Comma-separated list of host/domain names that this Django site can serve.                              | `localhost,127.0.0.1,your.domain.com` |
| `CORS_ALLOWED_ORIGINS`| Comma-separated list of origins that are allowed to make cross-site HTTP requests.                      | `http://localhost:8080,https://your.frontend.com` |
| `POSTGRES_DB`         | PostgreSQL database name.                                                                               | `ctf_db`                       |
| `POSTGRES_USER`       | PostgreSQL database user.                                                                               | `ctf_user`                     |
| `POSTGRES_PASSWORD`   | PostgreSQL database password.                                                                           | `ctf_pass`                     |
| `POSTGRES_HOST`       | PostgreSQL host. In Docker Compose, this is the service name (`db`).                                   | `db`                           |
| `POSTGRES_PORT`       | PostgreSQL port.                                                                                        | `5432`                         |
| `REDIS_URL`           | Redis connection URL for Django Channels. In Docker Compose, this is `redis://redis:6379/1`.            | `redis://redis:6379/1`         |

## Production Deployment (Docker Compose)

For a simple production deployment using Docker Compose, you would typically:

1.  **Set `DJANGO_DEBUG=False`** in your `.env` file.
2.  **Update `DJANGO_ALLOWED_HOSTS`** with your production domain(s) and IP addresses.
3.  **Update `CORS_ALLOWED_ORIGINS`** to your production frontend URL(s).
4.  **Ensure `DJANGO_SECRET_KEY`** is a strong, randomly generated value and kept secret.
5.  **Run Docker Compose:**
    ```bash
    docker-compose -f docker-compose.yml up --build -d
    ```
    The `backend` service's `command` will automatically run `collectstatic` and `migrate`. Nginx in the `frontend` service is configured to serve the Vue.js static assets and reverse proxy API and WebSocket requests to the `backend` service.

## Production Deployment (Kubernetes)

Deploying to Kubernetes involves creating several manifest files to define your application's components and how they run in the cluster.

### Key Kubernetes Objects
*   **Deployment:** Defines how to run your application containers (e.g., `backend`, `frontend`, `db`, `redis`). It manages replica sets and ensures a specified number of pods are always running.
*   **Service:** An abstract way to expose an application running on a set of Pods as a network service. For internal communication (e.g., `backend` to `db`), ClusterIP services are used. For external access, LoadBalancer or NodePort services are used, often combined with an Ingress.
*   **PersistentVolumeClaim (PVC):** Requests persistent storage for stateful applications like PostgreSQL, ensuring data survives pod restarts.
*   **Ingress:** Manages external access to services in a cluster, typically HTTP/S, by providing HTTP and HTTPS routing to services based on hostname or URL path.
*   **ConfigMap:** Stores non-confidential configuration data in key-value pairs.
*   **Secret:** Stores sensitive information, such as passwords and API keys.

### Example YAML Manifests (Illustrative)

These are basic examples. A full production setup would involve more robust configurations (e.g., resource limits, health probes, readiness probes, Horizontal Pod Autoscalers, etc.).

**1. `ctf-namespace.yaml`**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ctf-platform
```

**2. `ctf-secrets.yaml`**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ctf-backend-secret
  namespace: ctf-platform
type: Opaque
stringData:
  DJANGO_SECRET_KEY: "your_super_secret_key_here" # Replace with a strong secret
  POSTGRES_USER: "ctf_user"
  POSTGRES_PASSWORD: "ctf_pass"
  # Add other sensitive environment variables here
---
apiVersion: v1
kind: Secret
metadata:
  name: ctf-db-secret
  namespace: ctf-platform
type: Opaque
stringData:
  POSTGRES_PASSWORD: "ctf_pass" # Separate password for PostgreSQL internal use
```

**3. `ctf-configmap.yaml`**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ctf-backend-config
  namespace: ctf-platform
data:
  DJANGO_DEBUG: "False" # Set to False for production
  DJANGO_ALLOWED_HOSTS: "your.domain.com,www.your.domain.com"
  CORS_ALLOWED_ORIGINS: "https://your.frontend.com"
  POSTGRES_DB: "ctf_db"
  POSTGRES_HOST: "ctf-db" # Name of the DB service
  POSTGRES_PORT: "5432"
  REDIS_URL: "redis://ctf-redis:6379/1" # Name of the Redis service
```

**4. `postgres-pvc.yaml`**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ctf-postgres-pvc
  namespace: ctf-platform
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi # Request 5 GB of storage
```

**5. `ctf-db-deployment.yaml` & `ctf-db-service.yaml`**
```yaml
# ctf-db-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-db
  namespace: ctf-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ctf-db
  template:
    metadata:
      labels:
        app: ctf-db
    spec:
      containers:
        - name: postgres
          image: postgres:15-alpine
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: ctf-backend-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: ctf-backend-secret
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: ctf-db-secret
                  key: POSTGRES_PASSWORD
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
          ports:
            - containerPort: 5432
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: ctf-postgres-pvc
---
# ctf-db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ctf-db
  namespace: ctf-platform
spec:
  selector:
    app: ctf-db
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP
```

**6. `ctf-redis-deployment.yaml` & `ctf-redis-service.yaml`**
```yaml
# ctf-redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-redis
  namespace: ctf-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ctf-redis
  template:
    metadata:
      labels:
        app: ctf-redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
          args: ["--appendonly", "yes"] # Enable persistence
          volumeMounts:
            - name: redis-storage
              mountPath: /data
      volumes:
        - name: redis-storage
          emptyDir: {} # For simple deployments, or use PVC for production Redis
---
# ctf-redis-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ctf-redis
  namespace: ctf-platform
spec:
  selector:
    app: ctf-redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP
```

**7. `ctf-backend-deployment.yaml` & `ctf-backend-service.yaml`**
```yaml
# ctf-backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-backend
  namespace: ctf-platform
spec:
  replicas: 2 # Scale as needed
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
          image: your-dockerhub-username/ctf-backend:latest # Push your backend image here
          envFrom:
            - configMapRef:
                name: ctf-backend-config
            - secretRef:
                name: ctf-backend-secret
          ports:
            - containerPort: 8000
          volumeMounts:
            - name: media-storage
              mountPath: /app/media
            - name: static-storage
              mountPath: /app/staticfiles
          # Add readiness and liveness probes
          readinessProbe:
            httpGet:
              path: /api/health/ # Implement a simple health check endpoint
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /api/health/
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 15
          command: ["/bin/sh", "-c"] # Override default CMD to run migrations first
          args:
            - |
              python manage.py makemigrations api &&
              python manage.py migrate --noinput &&
              python manage.py collectstatic --noinput &&
              daphne -b 0.0.0.0 -p 8000 ctf_platform.asgi:application
      volumes:
        - name: media-storage
          emptyDir: {} # For production, use PVC for media
        - name: static-storage
          emptyDir: {} # For production, use PVC or initContainer for static files
---
# ctf-backend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ctf-backend
  namespace: ctf-platform
spec:
  selector:
    app: ctf-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

**8. `ctf-frontend-deployment.yaml` & `ctf-frontend-service.yaml`**
```yaml
# ctf-frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ctf-frontend
  namespace: ctf-platform
spec:
  replicas: 2 # Scale as needed
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
          image: your-dockerhub-username/ctf-frontend:latest # Push your frontend image here
          ports:
            - containerPort: 80
          # Add readiness and liveness probes
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 10
---
# ctf-frontend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ctf-frontend-service
  namespace: ctf-platform
spec:
  selector:
    app: ctf-frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP # Expose via Ingress
```

**9. `ctf-ingress.yaml`**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ctf-ingress
  namespace: ctf-platform
  annotations:
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "3600"
    nginx.ingress.kubernetes.io/websocket-services: "ctf-backend" # For WebSocket proxying
    # Add cert-manager annotations for TLS if using HTTPS
    # cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx # Or your ingress controller's class name
  rules:
    - host: your.domain.com # Replace with your domain
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: ctf-backend
                port:
                  number: 8000
          - path: /ws(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: ctf-backend
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ctf-frontend-service
                port:
                  number: 80
  # tls: # Uncomment for HTTPS
  #   - hosts:
  #       - your.domain.com
  #     secretName: your-tls-secret # K8s secret for your TLS certificate
```

### Deployment Steps (Kubernetes)

1.  **Build and push Docker images:**
    ```bash
    docker build -t your-dockerhub-username/ctf-backend:latest -f backend.Dockerfile .
    docker push your-dockerhub-username/ctf-backend:latest

    docker build -t your-dockerhub-username/ctf-frontend:latest -f frontend.Dockerfile .
    docker push your-dockerhub-username/ctf-frontend:latest
    ```
    (Replace `your-dockerhub-username` with your actual Docker Hub username or image registry).

2.  **Apply Kubernetes manifests:**
    ```bash
    kubectl apply -f ctf-namespace.yaml
    kubectl apply -f ctf-secrets.yaml
    kubectl apply -f ctf-configmap.yaml
    kubectl apply -f postgres-pvc.yaml
    kubectl apply -f ctf-db-deployment.yaml
    kubectl apply -f ctf-db-service.yaml
    kubectl apply -f ctf-redis-deployment.yaml
    kubectl apply -f ctf-redis-service.yaml
    kubectl apply -f ctf-backend-deployment.yaml
    kubectl apply -f ctf-backend-service.yaml
    kubectl apply -f ctf-frontend-deployment.yaml
    kubectl apply -f ctf-frontend-service.yaml
    kubectl apply -f ctf-ingress.yaml
    ```

3.  **Monitor deployments:**
    ```bash
    kubectl get pods -n ctf-platform
    kubectl get svc -n ctf-platform
    kubectl get ingress -n ctf-platform
    ```

4.  **Create superuser (if not using an init container or pre-baked DB image):**
    Find the `ctf-backend` pod name and execute:
    ```bash
    kubectl exec -it <backend-pod-name> -n ctf-platform python manage.py createsuperuser
    ```

## Managing Dockerized Challenges

The current implementation focuses on static challenges with optional file attachments. For truly "dockerized" dynamic challenges where each team gets an isolated instance (e.g., King of the Hill, Attack-Defense), the platform blueprint specifies:

*   **Dynamic Challenge Management:** Interface to manage dynamic challenge templates and resource monitoring.

The workflow would involve:
1.  **Admin uploads challenge template:** An administrator defines a challenge in the Django admin, marks it as `is_dynamic=True`, and potentially uploads a Docker Compose file or a Kubernetes manifest template as part of the challenge's file attachment.
2.  **Platform provisions instance:** When a user starts a dynamic challenge, the backend would:
    *   Parse the uploaded template.
    *   Use a container orchestration API (Docker Swarm API or Kubernetes API) to deploy a dedicated instance of the challenge for the user/team.
    *   Generate a unique flag for the instance and update the `Challenge` model (or a related `ChallengeInstance` model) with this flag and instance connection details.
    *   Expose the challenge instance (e.g., via a unique port or subdomain).
3.  **User interacts with instance:** The user connects to their unique challenge instance, solves it, and submits the flag.
4.  **Platform tears down instance:** After solve, or a timeout, the instance is cleaned up.

**Note:** This "Managing Dockerized Challenges" section describes the *intended advanced functionality* as per the project blueprint. The current code provides the data models for dynamic challenges (`initial_points`, `minimum_points`, `decay_factor`) and the `is_dynamic` flag, but the actual orchestration logic for provisioning and managing external containers is a complex feature that would be built atop this foundation.


---

# CONTRIBUTING.md
# Contributing to the CTF Platform

We welcome contributions to the CTF Platform! Whether you're fixing a bug, adding a new feature, or improving documentation, your help is appreciated. Please read these guidelines to ensure a smooth contribution process.

## Getting Started

To set up your local development environment without Docker (for direct code changes and faster iteration):

### Backend Setup (Django)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ctf-platform.git
    cd ctf-platform
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up PostgreSQL:**
    Ensure you have a PostgreSQL server running locally (e.g., via `brew postgresql start` on macOS, or a Docker container for just the DB). Create a database and user for the project, matching the settings in `ctf_platform/settings.py` (or provide them via environment variables if you set up a `.env` file).

5.  **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start the Django development server:**
    ```bash
    # For HTTP (API endpoints)
    python manage.py runserver 0.0.0.0:8000
    # For WebSockets (Channels)
    daphne -b 0.0.0.0 -p 8000 ctf_platform.asgi:application
    # Note: For full Channels functionality in dev, you need to run Redis (e.g., via `docker run -p 6379:6379 redis:latest`)
    # and then run the Daphne server.
    ```
    If you are running the frontend concurrently, you would typically run Daphne, and the frontend will connect to it.

### Frontend Setup (Vue.js)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Start the Vue.js development server:**
    ```bash
    npm run dev
    ```
    The frontend will typically be available at `http://localhost:8080`. It will proxy API requests to your Django backend (running on `http://localhost:8000` by default).

## Code Style

Consistency is key! Please adhere to the following style guidelines:

*   **Python:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code. We recommend using `flake8` or `black` for linting/formatting.
*   **Vue.js/JavaScript:**
    *   Use a consistent coding style, preferably following [Prettier](https://prettier.io/) defaults for formatting.
    *   Use Vue 3 Composition API with `<script setup>`.
    *   Ensure proper component naming (PascalCase for files, kebab-case for usage).
    *   Keep components focused and reusable.

## Backend Development

### Migrations
Whenever you make changes to `api/models.py` or any other Django app's models, you need to create and apply database migrations:
1.  **Create migration files:**
    ```bash
    python manage.py makemigrations api # Or your specific app name
    ```
2.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

### Running Tests
To ensure your changes haven't introduced regressions, run the Django test suite:
```bash
python manage.py test api # Or test specific apps/modules
```

## Commit & Pull Request Process

1.  **Branching:** Create a new branch for each feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/issue-description
    ```
2.  **Commit messages:** Write clear and concise commit messages. A good commit message explains *what* was changed and *why*.
3.  **Push your branch:**
    ```bash
    git push origin feature/your-feature-name
    ```
4.  **Create a Pull Request (PR):**
    *   Open a PR from your branch to the `main` branch.
    *   Provide a clear description of your changes, including any relevant issue numbers.
    *   Ensure your code passes all tests and follows the style guidelines.
    *   Be responsive to feedback during the code review process.

Thank you for your contributions!
```
