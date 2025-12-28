"""
Startup script that fixes asyncio event loop policy before starting the server.
This fixes the NotImplementedError with Playwright on Windows/Anaconda.
"""
import sys
import asyncio
import os

# CRITICAL: Set event loop policy BEFORE importing anything that uses asyncio
if sys.platform == 'win32':
    try:
        # Force WindowsSelectorEventLoopPolicy for Playwright compatibility
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print("[OK] Event loop policy set for Playwright compatibility")
    except Exception as e:
        print(f"[WARNING] Could not set event loop policy: {e}")

# Now import and run uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

