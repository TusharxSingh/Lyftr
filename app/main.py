import sys
import asyncio
import os

# CRITICAL: Set event loop policy BEFORE any other imports that might create event loops
# This fixes the NotImplementedError with Playwright on Windows/Anaconda
if sys.platform == 'win32':
    try:
        # Force WindowsSelectorEventLoopPolicy for Playwright compatibility
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        # Create a new event loop with the correct policy
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except Exception:
        # If setting policy fails, continue anyway
        pass

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader

from app.api import health, scrape

app = FastAPI(title="AI Web Scraper", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(scrape.router)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_dir))

# Serve frontend at /
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    template = jinja_env.get_template("index.html")
    return HTMLResponse(content=template.render())

