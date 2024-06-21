# Inventory Management

## Basic Installation

### Requirements
1. Python interpreter
2. pip

### Steps
1. Create a virtual environment
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Make migrations:
    ```bash
    python manage.py makemigrations
    ```
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Docker Installation

### Requirements
1. Docker
2. Docker-Compose

### Steps
1. Build and run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

## Note
The `Dockerfile` and `docker-compose.yml` are set up for basic testing of the application.

## Documentation
Swagger and Redoc documentation for the endpoints are available at the base path `/` and `/redoc/` respectively.
