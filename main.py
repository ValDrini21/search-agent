import os

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app
from middleware import jwt_middleware

# Configuration
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_SERVICE_URI = "sqlite:///./sessions.db"
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:3000", "http://localhost:8000", "*"]
SERVE_WEB_INTERFACE = False

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

 # Add JWT middleware
app.middleware("http")(jwt_middleware)

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "search-agent", "version": "1.1.8"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


# Since we are using FastAPI, we can declare even other routes outside of the adk agent routes
# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World from FastAPI!"}
