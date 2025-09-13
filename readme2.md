New and modified files for this step:

*   `README.md` (New)
*   `CONTRIBUTING.md` (New)

### `README.md`

```markdown
# CTF Platform

This repository contains the source code for a complete, feature-rich, and secure Capture The Flag (CTF) platform. It is built with a modern technology stack, featuring a FastAPI backend and a Vue.js frontend, designed for easy deployment and scalability.

## Features

This platform includes a wide range of features for both participants and administrators, based on the final project audit.

### User-Facing Features
- **User Authentication:** Secure registration with local accounts (email/password) and Social Logins (Google OAuth 2.0).
- **Email Verification:** Automated email verification for new accounts.
- **Team Management:** Users can create, browse, join, and leave teams.
- **User Profiles:** Public profiles display user scores, team affiliation, and earned badges.
- **Notifications:** In-app notifications for key events like earning a badge or account approval.
- **Live Activity Feed:** A real-time WebSocket feed on the homepage showing recent solves.
- **Event Countdown:** A dynamic timer on the homepage showing the time until the event starts or ends.

### Gameplay & Scoring
- **Challenge Board:** A grid-based view of all challenges.
- **Challenge Dependencies:** Ability to lock challenges until prerequisites are solved.
- **Flag Submission:** Secure, rate-limited flag submission endpoint.
- **Scoring System:** Backend support for both static and dynamic scoring models.
- **Leaderboard:** A real-time leaderboard ranking teams by score and submission time.
- **Trophies/Badges:** An achievement system that can award badges for special events, such as "First Blood" for the first solve of a challenge.
- **Write-up Submissions:** Users can submit write-ups for solved challenges.

### Admin Dashboard
- **Dashboard:** A central view with key platform statistics (total users, challenges, solves).
- **Platform Configuration:** A settings panel to manage the event title, theme, start/end times, and toggle features like registrations and teams.
- **User Management:** Full CRUD operations on users, including a queue for manual account verification.
- **Mass Management:** Tools for administrators, including a mass email utility to contact all registered users.
- **Challenge Management:** Full CRUD operations on challenges, including managing dependencies, tags, visibility, and scoring parameters.
- **Write-up Moderation:** A queue for administrators to review, approve, or reject user-submitted write-ups.
- **Platform Health & Logs:** A detailed, searchable Audit Log to track all significant platform events for security and forensics.

---

## Technology Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy (ORM), Alembic (Migrations), Pydantic (Validation)
- **Frontend:** Vue.js 3 (Composition API), Pinia (State Management), Vue Router, Tailwind CSS
- **Database:** PostgreSQL
- **Cache & Rate Limiting:** Redis
- **Authentication:** JWT with Passlib, OAuth 2.0 with Authlib
- **Real-time:** FastAPI WebSockets
- **Security:** Rate limiting with `slowapi`
- **Containerization:** Docker & Docker Compose
- **Web Server/Proxy:** Nginx

---

## Prerequisites

To run this project locally, you will need the following installed on your machine:
- Docker
- Docker Compose

---

## Local Development Setup

Follow these steps to get the entire application stack running on your local machine.

**1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Create an Environment File**
Create a `.env` file at the project root. This file will be used by `docker-compose.yml` to configure the services. You can copy the example below.

```dotenv
# .env

# PostgreSQL Settings
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=ctf_platform

# Backend Settings
SECRET_KEY=a_very_secret_and_secure_key_for_jwt_please_change_me
DATABASE_URL=postgresql://user:password@db/ctf_platform
REDIS_URL=redis://redis:6379

# Google OAuth 2.0 Settings (Optional)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email Settings (Optional, for registration emails)
MAIL_USERNAME=your_smtp_username
MAIL_PASSWORD=your_smtp_password
MAIL_FROM=noreply@yourdomain.com
MAIL_PORT=587
MAIL_SERVER=smtp.yourprovider.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

**3. Build and Run the Services**
Use Docker Compose to build the images and start all the containers (database, Redis, backend, frontend).

```bash
docker-compose up --build -d
```
The `-d` flag runs the containers in detached mode.

**4. Run Database Migrations**
The first time you start the application, the database will be empty. You need to apply the database schema using Alembic.

```bash
docker-compose exec backend alembic upgrade head
```

**5. Access the Application**
You should now be able to access the platform:
- **Frontend:** `http://localhost:8080`
- **Backend API:** `http://localhost:8080/api/` (via the Nginx reverse proxy)
- **API Docs:** `http://localhost:8080/api/docs`

---

## Configuration

The following environment variables are used to configure the application:

| Variable                | Description                                                | Service         |
|-------------------------|------------------------------------------------------------|-----------------|
| `POSTGRES_USER`         | The username for the PostgreSQL database.                  | `db`            |
| `POSTGRES_PASSWORD`     | The password for the PostgreSQL database.                  | `db`            |
| `POSTGRES_DB`           | The name of the database to use.                           | `db`            |
| `SECRET_KEY`            | A secret key used for signing JWTs and sessions.           | `backend`       |
| `DATABASE_URL`          | The full connection string for the PostgreSQL database.    | `backend`       |
| `REDIS_URL`             | The connection string for the Redis instance.              | `backend`       |
| `GOOGLE_CLIENT_ID`      | The client ID for Google OAuth 2.0.                        | `backend`       |
| `GOOGLE_CLIENT_SECRET`  | The client secret for Google OAuth 2.0.                    | `backend`       |
| `MAIL_USERNAME`         | The username for your SMTP email server.                   | `backend`       |
| `MAIL_PASSWORD`         | The password for your SMTP email server.                   | `backend`       |
| `MAIL_FROM`             | The "from" address for outgoing emails.                    | `backend`       |
| `MAIL_PORT`             | The port for the SMTP server.                              | `backend`       |
| `MAIL_SERVER`           | The hostname or IP address of the SMTP server.             | `backend`       |
| `MAIL_STARTTLS`         | Whether to use STARTTLS (boolean).                         | `backend`       |
| `MAIL_SSL_TLS`          | Whether to use SSL/TLS (boolean).                          | `backend`       |


---

## Production Deployment

### Using Docker Compose
For a simple, single-server deployment, you can adapt the provided `docker-compose.yml`.
1.  **Use a strong `SECRET_KEY`** in your `.env` file.
2.  **Remove development volumes:** In `docker-compose.yml`, remove the volume mounts that sync your local source code (e.g., `- ./app:/app/app`) to ensure you are running the code built into the Docker image.
3.  **Configure Nginx for your domain:** Update `nginx.conf` and `docker-compose.yml` to use your domain name and handle SSL/TLS termination, preferably with Certbot/Let's Encrypt.
4.  Run `docker-compose up --build -d`.

### Using Kubernetes (K8s)
For a scalable, resilient deployment, Kubernetes is recommended. A high-level overview of the required components includes:
- **Secrets & ConfigMaps:** To manage database credentials, API keys, and other configuration data securely.
- **PersistentVolumeClaim:** To provide stable storage for the PostgreSQL database.
- **Deployments:** For the `backend`, `frontend`, `db`, and `redis` services, defining replicas, resource limits, and update strategies.
- **Services:** To expose the deployments within the cluster (e.g., a ClusterIP service for the backend so the frontend can reach it).
- **Ingress:** An Ingress controller (like Nginx Ingress or Traefik) to manage external access to the frontend and backend services, handle SSL termination, and route traffic based on hostnames or paths.
```

### `CONTRIBUTING.md`

```markdown
# Contributing to the CTF Platform

We welcome contributions from the community! This document provides guidelines for developers who want to contribute to the project.

## Getting Started (Without Docker)

For developers who prefer to run services on their local machine without Docker, follow these steps.

### Backend (FastAPI)
1.  **Prerequisites:** Ensure you have Python 3.11+ and PostgreSQL installed and running.
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Environment Variables:** You must set the required environment variables in your shell for the application to connect to the database and Redis.
    ```bash
    export DATABASE_URL="postgresql://user:password@localhost/ctf_platform"
    export REDIS_URL="redis://localhost:6379"
    export SECRET_KEY="some-local-dev-secret-key"
    # Set other variables for email/OAuth as needed
    ```
5.  **Run Database Migrations:**
    ```bash
    alembic upgrade head
    ```
6.  **Run the Development Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be available at `http://127.0.0.1:8000`.

### Frontend (Vue.js)
1.  **Prerequisites:** Ensure you have Node.js (LTS version) and npm installed.
2.  **Navigate to the Frontend Directory:**
    ```bash
    cd frontend
    ```
3.  **Install Dependencies:**
    ```bash
    npm install
    ```
4.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173` (or another port if 5173 is busy) with hot-reloading enabled. The Vite server is pre-configured to proxy API requests to `http://127.0.0.1:8000`.

---

## Code Style

- **Python/Backend:** We adhere to the **Black** code style. Please format your code before committing.
- **Vue/Frontend:** We use **Prettier** for consistent code formatting. It is recommended to use a Prettier extension in your code editor to format on save.

---

## Backend Development

### Database Migrations
This project uses Alembic to manage database schema changes. When you modify a SQLAlchemy model in `app/models.py`, you must generate a new migration script.

1.  **Make your changes** to the models.
2.  **Generate the migration script:**
    ```bash
    alembic revision --autogenerate -m "A short, descriptive message about the changes"
    ```
3.  **Review the generated script** in `alembic/versions/` to ensure it is correct.
4.  **Apply the migration** to your local database:
    ```bash
    alembic upgrade head
    ```

---

## Running Tests

While tests were not implemented in the initial build, they are a crucial part of the development process.
- **Backend tests** should be written using `pytest` and placed in a `tests/` directory.
- **Frontend tests** can be written using a framework like Vitest.

To run the test suite (once implemented):
```bash
# For backend
pytest

# For frontend
npm run test
```

---

## Commit & Pull Request Process

1.  **Fork the repository** and clone it to your local machine.
2.  **Create a new branch** for your feature or bugfix: `git checkout -b feature/my-awesome-feature`.
3.  **Make your changes.** Write clean, well-commented code.
4.  **Commit your changes** with a clear and descriptive commit message.
5.  **Push your branch** to your fork: `git push origin feature/my-awesome-feature`.
6.  **Open a Pull Request** against the `main` branch of the original repository. Provide a detailed description of the changes you made.
```
