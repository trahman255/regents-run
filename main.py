from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origins
origins = [
    "*",  # Allows all origins (easiest for development and deployment)
    # Or restrict specifically later, e.g.:
    # "http://localhost:3000",
    # "http://localhost:5500",
    # "http://127.0.0.1:5500",
    # "https://your-frontend.vercel.app",
    # "https://your-frontend.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing routes/endpoints follow below...