from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from database import init_db
from routes import router

# Create FastAPI app
app = FastAPI(title="Driftwood LLM Simulation Lab", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the main HTML file"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Driftwood LLM Simulation Lab - Backend Running"}

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 