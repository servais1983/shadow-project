from fastapi import FastAPI
from src.api.routes import social, legal
from src.scraping.twitter import search_twitter
from src.ai.face_scan import scan_image

app = FastAPI(title="Shadow API")

@app.get("/")
def root():
    return {"status": "OK", "message": "Shadow API is running"}

# Include routers from different modules
app.include_router(social.router, prefix="/social")
app.include_router(legal.router, prefix="/legal")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
