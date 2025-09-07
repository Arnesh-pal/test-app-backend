# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models, database
from .routers import auth, exams

# This command ensures all your tables are created when the app starts
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- CORRECT CORS CONFIGURATION ---
# This section acts as a security guard, telling your backend
# that it's okay to accept requests from your React app.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers (like Authorization)
)
# ------------------------------------

# Include the routers for your endpoints
app.include_router(auth.router)
app.include_router(exams.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exam App API"}