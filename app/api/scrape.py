from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx

from app.core.heuristic import should_use_js_scraper
from app.core.static_scraper import scrape_static
from app.core.js_scraper import scrape_js
from app.core.section_parser import parse_sections
from app.models.schema import ScrapeResponse

router = APIRouter(tags=["scrape"])

class ScrapeRequest(BaseModel):
    url: HttpUrl

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_url(request: ScrapeRequest):
    import traceback
    try:
        url = str(request.url)
        
        # Determine scraping strategy
        use_js = await should_use_js_scraper(url)
        
        html_content = None
        
        # Try JS scraper first if needed, with fallback to static
        if use_js:
            try:
                html_content = await scrape_js(url)
            except (NotImplementedError, ValueError) as e:
                # If Playwright fails (e.g., Anaconda asyncio issue), fall back to static
                if "Playwright subprocess" in str(e) or isinstance(e, NotImplementedError):
                    print(f"Warning: Playwright failed, falling back to static scraping: {e}")
                    html_content = await scrape_static(url)
                else:
                    raise
        
        if html_content is None:
            # Use static scraper
            html_content = await scrape_static(url)
        
        if not html_content or len(html_content.strip()) == 0:
            raise ValueError("No content retrieved from the URL")
        
        # Parse sections
        sections = parse_sections(html_content)
        
        return ScrapeResponse(
            url=url,
            sections=sections
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"HTTP error {e.response.status_code}: {e.response.reason_phrase}. The website may require authentication or is blocking requests."
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Request timeout. The website took too long to respond."
        )
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        
        # Log the full traceback for debugging (in production, use proper logging)
        print(f"ERROR: {error_type}: {error_msg}")
        print(traceback.format_exc())
        
        # Provide more helpful error messages
        if "net::ERR" in error_msg or "Navigation failed" in error_msg:
            error_msg = "Failed to navigate to the website. It may require authentication, be blocked, or be inaccessible."
        elif "timeout" in error_msg.lower():
            error_msg = "Request timed out. The website took too long to load."
        elif "AttributeError" in error_type or "'NoneType' object" in error_msg:
            error_msg = "Error parsing website content. The page structure may be unexpected."
        
        raise HTTPException(status_code=500, detail=f"Scraping failed: {error_msg}")

