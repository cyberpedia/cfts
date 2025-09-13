New and modified files for this step:

*   `CONTRIBUTING.md` (New)
*   `README.md` (New)

### `CONTRIBUTING.md`

```markdown
# Contributing to the CTF Platform

First off, thank you for considering contributing! This document provides guidelines for developers who want to contribute to the project.

## Getting Started

For a production-like setup, please refer to the `README.md` and use Docker Compose. The following instructions are for setting up the frontend and backend as separate services for local development without containers.

### Backend Development (FastAPI)

1.  **Prerequisites:**
    *   Python 3.10+
    *   A running PostgreSQL database instance.
    *   A running Redis instance.

2.  **Setup:**
    *   Navigate to the project root.
    *   Create and activate a Python virtual environment:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
        ```
    *   Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Set the necessary environment variables. You can create a `.env` file in the root directory:
        ```env
        SECRET_KEY=a_secure_random_string
        DATABASE_URL=postgresql://user:password@localhost:5432/ctf_platform
        REDIS_URL=redis://localhost:6379
        # Add other variables for Mail and OAuth as needed
        ```
    *   Run the database migrations:
        ```bash
        alembic upgrade head
        ```
    *   Start the development server:
        ```bash
        uvicorn app.main:app --reload
        ```
    *   The backend API will be available at `http://127.0.0.1:8000`.

### Frontend Development (Vue.js)

1.  **Prerequisites:**
    *   Node.js 20.x or later
    *   npm

2.  **Setup:**
    *   Navigate to the frontend directory:
        ```bash
        cd frontend
        ```
    *   Install the dependencies:
        ```bash
        npm install
        ```
    *   Start the development server:
        ```bash
        npm run dev
        ```
    *   The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use). It is pre-configured to proxy API requests to the backend at `http://127.0.0.1:8000`.

## Code Style

To maintain a consistent codebase, please adhere to the following style guides.

*   **Python (Backend):** We use **Black** for code formatting and **isort** for import sorting. Please run these tools on your code before committing.
*   **JavaScript/Vue (Frontend):** We use **Prettier** for code formatting. You can configure your editor to format on save, or run it manually.

## Backend Development

### Database Migrations

This project uses **Alembic** to manage database schema migrations. When you make changes to the SQLAlchemy models in `app/models.py`, you must generate a new migration script.

1.  **Make changes** to your models in `app/models.py`.
2.  **Generate a migration script:**
    ```bash
    alembic revision --autogenerate -m "A short, descriptive message of your changes"
    ```
3.  **Review the generated script** in `alembic/versions/` to ensure it accurately reflects your changes.
4.  **Apply the migration** to your local database:
    ```bash
    alembic upgrade head
    ```

## Running Tests

(Placeholder) A full test suite should be developed using `pytest`.

To run the backend tests, execute the following command:
```bash
pytest
```

Ensure that all new features are accompanied by corresponding tests and that all existing tests pass before submitting a pull request.

## Commit & Pull Request Process

1.  Create a new branch for your feature or bug fix from the `main` branch. (e.g., `feature/add-new-chart` or `fix/login-bug`).
2.  Make your changes and commit them with clear, descriptive messages.
3.  Ensure your code adheres to the style guides.
4.  If you've added new features, please update the documentation (`README.md`) if necessary.
5.  Push your branch to the repository and open a pull request against the `main` branch.
6.  Provide a clear description of the changes in your pull request.
```

### `README.md`

```markdown
# CTF Platform

A complete, feature-rich, and secure Capture The Flag (CTF) platform built with FastAPI and Vue.js. This project provides a modern, real-time environment for hosting jeopardy-style CTF competitions.

## Features

*   **User & Team Management**:
    *   Secure local user registration and authentication (JWT).
    *   Social logins with Google (OAuth 2.0).
    *   Email verification for new accounts.
    *   Team creation, joining, and leaving.
*   **Gameplay & Scoring**:
    *   Support for static and dynamic challenge scoring.
    *   Challenge dependencies (unlocking challenges by solving others).
    *   Trophies/Badges system, including "First Blood" awards.
    *   Secure, constant-time flag comparison.
    *   Write-up submission system.
*   **Real-Time Features**:
    *   Live activity feed showing real-time solves via WebSockets.
    *   Event countdown timer for start and end times.
*   **Admin Dashboard**:
    *   Comprehensive platform configuration (feature flags, event timing, UI).
    *   Full CRUD management for users, challenges, tags, and badges.
    *   User verification queue for manual approvals.
    *   Write-up moderation queue.
    *   Detailed, searchable audit log for all critical actions.
    *   Mass email tool to contact all registered users.
*   **Dynamic Challenges**:
    *   API for starting and stopping containerized challenges on demand.
*   **Security & Infrastructure**:
    *   Rate limiting on sensitive endpoints (login, registration, flag submission).
    *   Fully containerized with Docker and Docker Compose for easy deployment.
    *   Nginx reverse proxy for serving the frontend and directing API traffic.

## Technology Stack

*   **Backend**: Python, FastAPI, SQLAlchemy, Alembic, Pydantic, SlowAPI
*   **Frontend**: Vue.js 3 (Composition API), Pinia, Vue Router, Tailwind CSS, Axios
*   **Database**: PostgreSQL
*   **Cache/Rate Limiting**: Redis
*   **Containerization**: Docker, Docker Compose
*   **Web Server**: Uvicorn (backend), Nginx (frontend)

## Prerequisites

To run this project locally, you will need:
*   Docker
*   Docker Compose

## Local Development Setup

Follow these steps to get the entire platform running on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create an Environment File**
    Copy the example environment file. This will store your configuration variables.
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in the required variables, especially `SECRET_KEY`. See the **Configuration** section below for details on all variables.

3.  **Build and Run with Docker Compose**
    This command will build the Docker images for the frontend and backend, and start all services (database, Redis, backend, frontend) in the background.
    ```bash
    docker-compose up -d --build
    ```

4.  **Run Database Migrations**
    Once the backend container is running, execute the Alembic database migrations to set up the initial database schema.
    ```bash
    docker-compose exec backend alembic upgrade head
    ```

5.  **Access the Application**
    The CTF platform should now be running!
    *   **Frontend**: [http://localhost:8080](http://localhost:8080)
    *   **Backend API**: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)

## Configuration

All configuration is managed via environment variables. Create a `.env` file in the project root to set these values.

| Variable                      | Description                                                                 | Default                                            |
| ----------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------- |
| `SECRET_KEY`                  | **Required.** A long, random string for signing JWTs and sessions.              | `a_super_secret_key...` (Change this!)             |
| `DATABASE_URL`                | The connection string for the PostgreSQL database.                          | `postgresql://user:password@db/ctf_platform`       |
| `REDIS_URL`                   | The connection string for the Redis instance.                               | `redis://redis:6379`                               |
| `ALGORITHM`                   | The algorithm used for JWT signing.                                         | `HS256`                                            |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | The duration for which a JWT access token is valid.                         | `30`                                               |
| `MAIL_USERNAME`               | Username for the email sending service (e.g., SMTP).                        | `username`                                         |
| `MAIL_PASSWORD`               | Password for the email sending service.                                     | `password`                                         |
| `MAIL_FROM`                   | The "From" address for outgoing emails.                                     | `noreply@example.com`                              |
| `MAIL_PORT`                   | The port for the email server.                                              | `587`                                              |
| `MAIL_SERVER`                 | The address of the email server.                                            | `smtp.example.com`                                 |
| `MAIL_STARTTLS`               | Whether to use STARTTLS for the email connection.                           | `True`                                             |
| `MAIL_SSL_TLS`                | Whether to use SSL/TLS for the email connection.                            | `False`                                            |
| `GOOGLE_CLIENT_ID`            | The Client ID for Google OAuth 2.0.                                         | (empty)                                            |
| `GOOGLE_CLIENT_SECRET`        | The Client Secret for Google OAuth 2.0.                                     | (empty)                                            |

## Production Deployment

### Using Docker Compose

For small-scale deployments, you can adapt the provided `docker-compose.yml` file.
1.  **Use a managed database and Redis** service instead of running them in containers. Update the `DATABASE_URL` and `REDIS_URL` environment variables accordingly.
2.  **Remove the file `volumes`** from the `backend` service in `docker-compose.yml` to ensure you are running the code copied into the image, not the local code.
3.  **Use a robust secret management** system for your environment variables instead of a `.env` file.
4.  Run in detached mode: `docker-compose up -d`.

### Using Kubernetes (K8s)

For a scalable, production-grade deployment, Kubernetes is recommended. A high-level overview of the required components is as follows:

1.  **Container Registry**: Build and push the `backend` and `frontend` Docker images to a container registry (e.g., Docker Hub, GCR, ECR).
2.  **Stateful Services**:
    *   Deploy PostgreSQL and Redis using a managed cloud service (e.g., AWS RDS, Google Cloud SQL) or as `StatefulSet`s within your cluster.
3.  **Backend Deployment**:
    *   Create a `Deployment` for the backend service, pulling the image from your registry.
    *   Use a `Secret` to store all environment variables.
    *   Expose the deployment internally with a `Service`.
4.  **Frontend Deployment**:
    *   Create a `Deployment` for the Nginx/frontend service.
    *   Expose it with a `Service` of type `LoadBalancer` or `NodePort`.
5.  **Ingress**:
    *   Create an `Ingress` resource to manage external traffic. The Ingress controller will route requests to the frontend service and reverse proxy paths like `/api/` and `/ws/` to the backend service, handling TLS termination.
```
