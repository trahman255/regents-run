from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, tests

app = FastAPI()

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routers
app.include_router(auth.router)
app.include_router(tests.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Regents Run API is running"}