
README.md
code
Markdown
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# CTF Platform

This repository contains the source code for a complete, feature-rich, and secure Capture The Flag (CTF) platform built with a modern technology stack. It includes a full-featured user interface for players and a comprehensive admin dashboard for managing the event.

## Features

The platform is designed with both players and administrators in mind, offering a robust set of features to run a dynamic and engaging CTF event.

### User-Facing Features
*   **Authentication:** Secure local account registration and login, plus social sign-on with Google (OAuth 2.0).
*   **Email Verification:** New accounts receive a verification email to activate.
*   **Challenge Board:** A grid of challenges that visually indicates locked challenges based on dependencies.
*   **Flag Submission:** Real-time flag submission with immediate feedback and rate limiting.
*   **Dynamic Scoring:** (Backend support) Points can be configured to decrease as more teams solve a challenge.
*   **Challenge Dependencies:** Challenges can be locked until other prerequisite challenges are solved.
*   **Team Management:** Users can create, view, join, and leave teams.
*   **Live Leaderboard:** A real-time ranked scoreboard of all teams.
*   **User Profiles:** Public profiles display user scores and earned badges.
*   **Trophies/Badges:** An achievement system that awards badges for accomplishments (e.g., "First Blood" for the first solve).
*   **Notifications:** In-app notifications for events like earning a badge or getting an account approved.
*   **Live Activity Feed:** A homepage feed showing recent solves from across the platform in real-time via WebSockets.
*   **Dynamic Challenges:** Support for starting and stopping containerized challenges on-demand.
*   **Write-up Submissions:** Users can submit write-ups for challenges they have solved.

### Admin Dashboard Features
*   **Dashboard:** A central view with key platform statistics (total users, challenges, solves).
*   **Platform Configuration:** A settings panel to control:
    *   Feature Flags (registrations, teams, write-ups).
    *   Event Timing (start and end times).
    *   UI Customization (event title, theme).
*   **User Management:** Full CRUD (Create, Read, Update, Delete) capabilities for all users.
*   **User Verification Queue:** Admins can manually view and approve pending user registrations.
*   **Challenge Management:** Full CRUD for challenges, including managing dependencies, tags, visibility, and scoring parameters.
*   **Write-up Moderation:** A queue for admins to review, approve, or reject submitted write-ups.
*   **Badge Management:** Full CRUD for the achievement badges available on the platform.
*   **Mass Management:** Tools for bulk actions, such as sending a mass email to all registered users.
*   **Detailed Audit Log:** An immutable log that tracks all critical security and gameplay events for forensics.

## Technology Stack

*   **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic, `slowapi` (rate limiting)
*   **Frontend:** Vue.js 3 (Composition API), Pinia, Vue Router, Axios, Tailwind CSS
*   **Real-time:** FastAPI WebSockets, `reconnecting-websocket` (client)
*   **Database:** PostgreSQL
*   **Cache/Rate Limiting:** Redis
*   **Containerization:** Docker & Docker Compose
*   **Web Server/Proxy:** Nginx

## Prerequisites

To run this project locally, you will need the following installed on your machine:
*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

## Local Development Setup

Follow these steps to get the entire platform running on your local machine.

**1. Clone the Repository**
```bash
git clone <your-repository-url>
cd <repository-directory>

2. Configure Environment Variables
Create a .env file in the project root by copying the example. This file will store secrets and configuration details.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# Create the .env file
touch .env

Now, open .env and add the following variables. Replace the placeholder values as needed.

code
Env
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# PostgreSQL Settings
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=ctf_platform

# FastAPI Backend Settings
# Generate a secure key with: openssl rand -hex 32
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
DATABASE_URL=postgresql://user:password@db/ctf_platform
REDIS_URL=redis://redis:6379

# Google OAuth Settings (Optional)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Email Settings (Optional, for registration emails)
MAIL_USERNAME=your_smtp_username
MAIL_PASSWORD=your_smtp_password
MAIL_FROM=noreply@yourdomain.com
MAIL_PORT=587
MAIL_SERVER=smtp.yourprovider.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

3. Build and Run with Docker Compose
This command will build the backend and frontend images and start all the services (db, redis, backend, frontend).

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose up --build

The frontend will be accessible at http://localhost:8080, and it will correctly proxy API requests to the backend.

4. Run Database Migrations
After the containers are up and running, open a new terminal window and run the Alembic database migrations to create all the necessary tables.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose exec backend alembic upgrade head

Your CTF platform is now fully running and accessible!

Configuration

All configuration is managed through environment variables, as detailed in the setup guide above.

Variable	Description
POSTGRES_USER	The username for the PostgreSQL database.
POSTGRES_PASSWORD	The password for the PostgreSQL database.
POSTGRES_DB	The name of the database to use.
SECRET_KEY	A secret key used for signing JWTs and sessions. Change this!
DATABASE_URL	The full connection string for the database, used by the backend.
REDIS_URL	The connection string for the Redis instance, used for rate limiting.
GOOGLE_CLIENT_ID	The client ID for Google OAuth 2.0 social logins.
GOOGLE_CLIENT_SECRET	The client secret for Google OAuth 2.0 social logins.
MAIL_*	A group of variables for configuring the SMTP server to send emails.
Production Deployment
Using Docker Compose

For a small-scale deployment, you can adapt the provided docker-compose.yml. Key changes would include:

Removing Code Volumes: Remove the volumes that mount local source code into the backend container to ensure you are running the code built into the image.

Production Uvicorn: Change the command for the backend service to run Uvicorn with multiple workers for better performance, e.g., uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4.

Secret Management: Move secrets from the .env file to a more secure secret management solution provided by your hosting environment.

Persistent Data: Ensure the postgres_data volume is backed up regularly.

Using Kubernetes (K8s)

For a scalable, production-grade deployment, Kubernetes is recommended. A high-level overview of the process is:

Container Registry: Build and push the backend and frontend Docker images to a container registry (e.g., Docker Hub, GCR, ECR).

Manifests: Create Kubernetes manifest files (.yaml) for the following resources:

StatefulSet for the PostgreSQL database, with a PersistentVolumeClaim for data storage.

Deployment for Redis.

Deployment for the backend service.

Deployment for the frontend (Nginx) service.

Services: ClusterIP or NodePort services to allow communication between pods.

ConfigMaps & Secrets: To manage environment variables and sensitive data like database passwords and API keys.

Ingress: An Ingress resource to manage external access to the frontend service and route API/WebSocket traffic, often paired with an Ingress controller like NGINX or Traefik.

code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
### `CONTRIBUTING.md`

```markdown
# Contributing to the CTF Platform

We welcome contributions to improve the platform! This guide will help you get your local development environment set up for making changes to either the backend or the frontend.

## Getting Started (Without Docker)

For more granular development, you might want to run the backend and frontend services directly on your host machine.

### Backend (FastAPI)

1.  **Prerequisites:**
    *   Python 3.11+
    *   PostgreSQL server running locally or accessible.
    *   Redis server running locally or accessible.

2.  **Setup:**
    ```bash
    # Create and activate a Python virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Configuration:**
    Set the required environment variables in your shell. The `DATABASE_URL` and `REDIS_URL` should point to your local instances.
    ```bash
    export SECRET_KEY='your-secret-key'
    export DATABASE_URL='postgresql://user:password@localhost/ctf_platform'
    export REDIS_URL='redis://localhost:6379'
    # ... set other variables for email/OAuth as needed
    ```

4.  **Run Migrations:**
    With your environment variables set, run the database migrations:
    ```bash
    alembic upgrade head
    ```

5.  **Run the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend API will now be running on `http://localhost:8000`.

### Frontend (Vue.js)

1.  **Prerequisites:**
    *   Node.js (v18 or later)
    *   npm

2.  **Setup & Run:**
    ```bash
    # Navigate to the frontend directory
    cd frontend

    # Install dependencies
    npm install

    # Run the development server
    npm run dev
    ```
    The Vue.js development server will start, typically on `http://localhost:5173`. It will automatically connect to the backend API running on port 8000.

## Code Style

To maintain a consistent codebase, we use the following formatters:
*   **Python:** Please format your code using [Black](https://github.com/psf/black).
*   **Frontend:** Please format your code using [Prettier](https://prettier.io/).

## Backend Development

### Database Migrations
We use Alembic to manage database schema changes. When you modify a SQLAlchemy model in `app/models.py`, you must generate a new migration script.

1.  **Generate Migration Script:**
    ```bash
    alembic revision --autogenerate -m "A short, descriptive message of your changes"
    ```
2.  **Apply Migration:**
    ```bash
    alembic upgrade head
    ```

## Running Tests

(Future Scope) To run the test suite, you would use `pytest`:```bash
pytest

Please ensure all existing tests pass and that you add new tests for any new functionality.

Commit & Pull Request Process

Fork the repository and create a new branch from main for your feature or bug fix.

Make your changes, adhering to the code style guidelines.

If you add new features, please add corresponding tests.

Ensure all tests pass.

Commit your changes with a clear and descriptive commit message.

Push your branch to your fork and open a Pull Request to the main repository.

In the Pull Request description, clearly explain the changes you made and why.

code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
