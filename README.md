# Instagram Django Live Invite System

## Description
This project is a Django-based application designed to interact with Instagram, specifically focusing on live invite functionalities. It incorporates features for managing user data, handling API interactions, and potentially scheduling tasks using Celery. The project is set up for both development and production environments using Docker and Nginx, indicating a robust and scalable architecture.

## Table of Contents
1. Introduction
2. Features
3. Technologies Used
4. Installation and Setup
5. Project Structure
6. Contributing
7. License
8. Contact




## 1. Introduction
The Instagram Django Live Invite System is a sophisticated web application built with Django, designed to automate and manage Instagram-related tasks, particularly those involving live invites. The system is engineered for high performance and scalability, utilizing Celery for asynchronous task processing and Docker for containerization. This setup allows for seamless deployment across various environments, from development to production, ensuring consistent performance and simplified management. The project aims to provide a comprehensive solution for interacting with Instagram APIs, handling user data, and managing scheduled operations efficiently.




## 2. Features
- **Instagram API Interaction**: Designed to interact with Instagram APIs for functionalities like live invites.
- **User Data Management**: Handles user-related data within the Django framework.
- **Asynchronous Task Processing**: Utilizes Celery for background tasks, improving application responsiveness.
- **Scheduled Tasks**: `django-celery-beat` suggests the ability to schedule recurring tasks.
- **Containerization**: Docker and Docker Compose for consistent development and production environments.
- **Production Deployment Ready**: Includes Nginx configuration and `docker-compose-prod.yml` for production deployments.
- **Story Reacting**: A commit message indicates a feature for reacting to stories.
- **Explore Page Updates**: Functionality to update the explore page for invites.
- **Error Handling**: Commit messages suggest fixes for data required issues and other crashes.




## 3. Technologies Used
- **Backend Framework**: Django (version 3.2.7)
- **Asynchronous Task Queue**: Celery (version 5.1.2)
- **Broker/Backend**: Redis (implied by `redis` in `requirements.txt`)
- **Database**: PostgreSQL (via `psycopg2` and `psycopg2-binary`)
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Containerization**: Docker, Docker Compose
- **Frontend**: HTML, CSS (including SCSS), JavaScript
- **Dependencies** (as per `requirements.txt`):
  - `amqp==5.0.6`
  - `anyjson==0.3.3`
  - `asgiref==3.4.1`
  - `billiard==3.6.4.0`
  - `celery==5.1.2`
  - `certifi==2021.5.30`
  - `charset-normalizer==2.0.6`
  - `click==7.1.2`
  - `click-didyoumean==0.0.3`
  - `click-plugins==1.1.1`
  - `click-repl==0.2.0`
  - `Django==3.2.7`
  - `django-celery-beat==2.2.1`
  - `django-crispy-forms`
  - `django-flatpickr==1.0.1`
  - `django-timezone-field==4.2.1`
  - `idna==3.2`
  - `kombu==5.1.0`
  - `prompt-toolkit==3.0.20`
  - `python-crontab==2.5.1`
  - `python-dateutil==2.8.2`
  - `pytz==2021.1`
  - `requests==2.26.0`
  - `six==1.16.0`
  - `sqlparse==0.4.2`
  - `urllib3==1.26.6`
  - `vine==5.0.0`
  - `wcwidth==0.2.5`
  - `redis`
  - `flower`
  - `psycopg2`
  - `psycopg2-binary`
  - `gunicorn`




## 4. Installation and Setup
This project leverages Docker and Docker Compose for both development and production environments, ensuring consistency and ease of deployment. Follow these steps to get the application running on your local machine:

### Prerequisites
- **Docker**: Ensure Docker Desktop (or Docker Engine) is installed and running on your system.
- **Docker Compose**: Docker Compose is usually bundled with Docker Desktop. Verify its installation.

### Steps for Development Environment
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/sherrywilly/InstagramDjangoliveInvite.git
    cd InstagramDjangoliveInvite
    ```

2.  **Build and run the Docker containers**:
    For development, you can use the default `docker-compose.yml`:
    ```bash
    docker-compose up --build
    ```
    This command will build the necessary Docker images (Django app, PostgreSQL, Redis, Celery) and start the services.

3.  **Run database migrations**:
    Once the containers are up and running, execute Django migrations to set up the database schema. You will need to run this command inside the running Django container:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Create a superuser** (optional, for admin access):
    To access the Django admin panel, create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to set up your administrator account.

5.  **Access the application**:
    The Django application should be accessible in your web browser, typically at `http://localhost:8000/`.
    Celery Flower (monitoring tool) might be available at `http://localhost:5555/`.

### Steps for Production Environment
For production deployment, the project includes a `docker-compose-prod.yml` and Nginx configuration.

1.  **Build and run production containers**:
    ```bash
    docker-compose -f docker-compose-prod.yml up --build -d
    ```
    The `-d` flag runs the containers in detached mode.

2.  **Run migrations and create superuser**:
    Similar to development, run migrations and create a superuser within the production web container:
    ```bash
    docker-compose -f docker-compose-prod.yml exec web python manage.py migrate
    docker-compose -f docker-compose-prod.yml exec web python manage.py createsuperuser
    ```

3.  **Collect static files**:
    For production, static files need to be collected:
    ```bash
    docker-compose -f docker-compose-prod.yml exec web python manage.py collectstatic --noinput
    ```

4.  **Access the application**:
    The application will be accessible via the Nginx proxy, typically on port 80 or 443, depending on your Nginx configuration and domain setup.

### Additional Scripts
- `connect.sh`: This script is likely used to connect to a specific service or container within the Docker environment (e.g., for debugging or shell access).
- `entry.sh` and `entrypoint.sh`: These scripts are likely entrypoints for the Docker containers, executing commands when the containers start up.




## 5. Project Structure
The project follows a well-organized structure, typical for a Django application integrated with Docker:

```
InstagramDjangoliveInvite/
├── .idea/                      # IDE configuration files (e.g., PyCharm)
├── app/                        # Django app for core application logic
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core/                       # Main Django project settings and configurations
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── instaDjangoApi/             # Django app for Instagram API interactions
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── nginx/                      # Nginx configuration files for production deployment
├── static/                     # Directory for static files (CSS, JavaScript, images)
├── templates/                  # Global templates directory
├── .gitignore                  # Specifies intentionally untracked files to ignore
├── Dockerfile                  # Dockerfile for building the Django application image
├── connect.sh                  # Script to connect to Docker containers (likely for database or shell access)
├── docker-compose-prod.yml     # Docker Compose configuration for production environment
├── docker-compose.yml          # Docker Compose configuration for development environment
├── entry.sh                    # Entrypoint script for the Docker container (development)
├── entrypoint.sh               # Entrypoint script for the Docker container (production)
├── manage.py                   # Django's command-line utility for administrative tasks
├── requirements.txt            # Python dependencies for the project
└── story.json                  # Likely a data file related to story functionalities
```




## 6. Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.




## 7. License
This project is licensed under the MIT License - see the `LICENSE` file for details.




## 8. Contact
For any questions or inquiries, please contact [sherrywilly](https://github.com/sherrywilly).


