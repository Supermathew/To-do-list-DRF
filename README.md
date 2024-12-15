# To-Do List Django DRF Project

## Project Overview
This is a Django REST Framework (DRF) based To-Do List application using PostgreSQL as the database.

## Prerequisites
- Python 3.8+
- pip
- PostgreSQL
- virtualenv (recommended)

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Supermathew/To-do-list-DRF.git
cd To-do-list-DRF
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
1. Create a PostgreSQL database
```sql
CREATE DATABASE tododb;
CREATE USER todoadmin WITH PASSWORD 'your_strong_password';
GRANT ALL PRIVILEGES ON DATABASE tododb TO todoadmin;
```

2. Update database settings in `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tododb',
        'USER': 'todoadmin',
        'PASSWORD': 'your_strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

### Development Server
```bash
python manage.py runserver
```

## Testing

### Running Tests
To run tests for specific apps:

```bash
# Run tests for accounts app
python manage.py test accounts

# Run tests for todo_app
python manage.py test todo_app

# Run all tests
python manage.py test
```

I'll provide a concise overview of the API endpoints.

## API Endpoints Overview

### Accounts Endpoints
1. **Register**: `/api/accounts/register/`
   - Create a new user account
   - Method: POST

2. **Login**: `/api/accounts/login/`
   - Authenticate user and get JWT tokens
   - Method: POST

3. **Token Refresh**: `/api/accounts/token/refresh/`
   - Get a new access token using refresh token
   - Method: POST

### Todo Task Endpoints
1. **Task List/Create**: `/api/task-api/tasks/`
   - List all tasks (GET)
   - Create new task (POST)
   - Requires: JWT Authentication

2. **Task Detail**: `/api/task-api/tasks/<task_id>/`
   - Retrieve a specific task (GET)
   - Update a task (PUT/PATCH)
   - Delete a task (DELETE)
   - Requires: JWT Authentication

3. **Delete All Tasks**: `/api/task-api/tasks/delete-all/`
   - Remove all user tasks
   - Method: DELETE
   - Requires: JWT Authentication

### Authentication Required
- All task-related endpoints need a valid JWT token
- Include token in Authorization header: `Bearer <access_token>`
