Spy Cat Agency (SCA) API
This is the backend API for the Spy Cat Agency (SCA), a system designed to manage spy cats, their missions, and the targets they are assigned to. It is a complete CRUD application built with FastAPI, PostgreSQL, and SQLAlchemy, featuring data validation, a full test suite, and integration with a third-party service.

Features
Cat Management: Create, list, update, and remove spy cats from the agency.

Mission Management: Create missions with 1-3 targets, assign cats to missions, and delete unassigned missions.

Target Updates: Update a target's notes and mark it as complete.

Automatic Mission Completion: Missions are automatically marked as complete once all their associated targets are completed.

Data Validation:

Validates request bodies to ensure data integrity.

Validates cat breeds against the official TheCatAPI.

Enforces business rules (e.g., a cat can only be on one mission at a time).

Database Migrations: Uses Alembic to manage database schema changes.

Comprehensive Testing: Includes a full test suite using Pytest to ensure API reliability.

Technologies Used
Backend Framework: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Database Migrations: Alembic

Data Validation: Pydantic

Testing: Pytest

HTTP Client: HTTPX

ASGI Server: Uvicorn

Getting Started
Follow these instructions to get the project up and running on your local machine.

1. Prerequisites
Python 3.8+

PostgreSQL installed and running.

An API key from TheCatAPI (optional, but recommended for full functionality).

2. Installation & Setup
Clone the repository:

```
git clone <your-repo-url>
cd spy_cat_agency
```

Create and activate a virtual environment:

# Create the environment
```
python -m venv venv
```

# Activate it (macOS/Linux)
```
source venv/bin/activate
```

# Activate it (Windows)
```
.\venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Configure environment variables:
Create a file named .env in the project root and add the following content. Replace the placeholder values with your actual database credentials and your API key.

# .env
DATABASE_URL="postgresql://YOUR_POSTGRES_USER:YOUR_POSTGRES_PASSWORD@localhost/spy_cat_db"
THECATAPI_API_KEY="your_thecatapi_key_here"

Create the PostgreSQL database:
Make sure to create a database with the name you specified in your DATABASE_URL (e.g., spy_cat_db).

3. Run Database Migrations
Before running the application for the first time, you need to create the database tables using Alembic.

# Generate the initial migration script
```
alembic revision --autogenerate -m "Initial migration with cats, missions, targets"
```

# Apply the migration to the database
```
alembic upgrade head
```

4. Running the Application
To start the API server, use Uvicorn:

```
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

You can now access the interactive Swagger UI documentation in your browser to test the endpoints:

http://127.0.0.1:8000/docs

5. Running the Tests
To run the automated test suite, use Pytest. The tests run against a separate, in-memory SQLite database and do not affect your PostgreSQL data.

From the project root directory, simply run:

```
pytest
```