from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- This was the missing line!
from routers import tests, auth
from core.database import engine
from models import domain

# This ensures all your tables are created in PostgreSQL
domain.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Regents Run API")

# --- CORS BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],
)
# ---------------------------

# Connect your route files
app.include_router(tests.router)
app.include_router(auth.router)