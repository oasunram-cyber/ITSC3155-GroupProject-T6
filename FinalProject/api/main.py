import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import index as index_router
from models import model_loader

app = FastAPI()

# Initialize Database Tables
model_loader.index()

# Load all routes
index_router.load_routes(app)

# Add CORS so your frontend/browser can talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
