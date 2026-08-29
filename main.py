from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers from the routers folder
# (Adjust the import names based on the files inside your 'routers/' directory)
from routers import questions  # or whatever your router file is named, e.g., tests, questions, etc.

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

# Mount the router to the FastAPI app
app.include_router(questions.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Regents Run API is running"}