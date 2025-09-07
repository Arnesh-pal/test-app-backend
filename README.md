Modern Exam App API
This repository contains the backend service for the Modern Exam App, a full-stack application for taking dynamic quizzes. This API is built with Python and FastAPI, handling user authentication, fetching questions from an external service, and storing detailed user exam history.

Live API Endpoint: https://etest-app-api.onrender.com

Features
JWT Authentication: Secure user registration and login using JSON Web Tokens.

Dynamic Question Fetching: Integrates with the QuizAPI.io to serve dynamic questions based on user-selected topics, difficulty, and limits.

Detailed History Tracking: Saves every exam attempt and each answered question to a persistent database.

Performance Analytics: Provides endpoints to retrieve a user's complete exam history and aggregated performance statistics by topic.

Cloud Deployment: Fully configured for deployment on Render with a PostgreSQL database on Neon.

Tech Stack
Framework: FastAPI

Database: PostgreSQL

Authentication: Python-JOSE (JWT) & Passlib (Hashing)

Hosting: Render

Database Hosting: Neon

API Endpoints
The interactive API documentation (Swagger UI) is available at the /docs endpoint of the live API.

Method

Endpoint

Description

Protected

POST

/auth/register

Create a new user account.

No

POST

/auth/token

Log in a user and receive a JWT.

No

GET

/exams/topics

Get a list of available exam topics.

Yes

GET

/exams/start

Fetch questions for a new exam.

Yes

POST

/exams/save_result

Save the results of a completed exam.

Yes

GET

/exams/history

Get a user's exam history and stats.

Yes

GET

/exams/history/{attempt_id}

Get details of a specific exam attempt.

Yes

Local Setup
To run this project locally, follow these steps:

Clone the repository:

git clone [https://github.com/Arnesh-pal/test-app-backend.git]
cd exam-app-backend

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Set up the database:

Make sure you have PostgreSQL running.

Connect to psql and create a database and user:

CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';
CREATE DATABASE examdb;
GRANT ALL PRIVILEGES ON DATABASE examdb TO myuser;

Configure Environment Variables:

Create a .env file in the root directory.

Copy the contents of .env.example (if provided) or add the variables manually:

DATABASE_URL="postgresql://myuser:mypassword@localhost/examdb"
QUIZ_API_KEY="your_quizapi_key_here"
SECRET_KEY="a_very_strong_random_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

Run the application:

uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000.