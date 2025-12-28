from playwright.async_api import async_playwright, Browser, Page
from app.util.url_util import validate_url
from app.util.noise_filter import remove_noise
from app.core.interactions import handle_interactions
import asyncio
import sys

async def scrape_js(url: str) -> str:
    """
    Playwright rendering with scroll + click flow
    """
    if not validate_url(url):
        raise ValueError(f"Invalid URL: {url}")
    
    # Ensure correct event loop policy for Windows/Anaconda
    if sys.platform == 'win32':
        try:
            current_policy = asyncio.get_event_loop_policy()
            if not isinstance(current_policy, asyncio.WindowsSelectorEventLoopPolicy):
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                ignore_https_errors=True
            )
            page = await context.new_page()
            
            try:
                # Navigate to page with better error handling
                try:
                    response = await page.goto(url, wait_until="networkidle", timeout=60000)
                    if response and response.status >= 400:
                        raise ValueError(f"HTTP {response.status}: Failed to load page. The website may require authentication or is blocking automated access.")
                except Exception as e:
                    if "net::ERR" in str(e) or "Navigation failed" in str(e):
                        raise ValueError(f"Failed to navigate to website: {str(e)}. The site may require authentication, be blocked, or be inaccessible.")
                    raise
                
                # Handle interactions (scroll, click, tabs, etc.)
                try:
                    await handle_interactions(page)
                except Exception:
                    # If interactions fail, continue with what we have
                    pass
                
                # Get HTML content
                html_content = await page.content()
                
                # Remove noise
                html_content = remove_noise(html_content)
                
                return html_content
            finally:
                await browser.close()
    except NotImplementedError as e:
        # Fallback: If Playwright can't create subprocess, raise a clear error
        raise ValueError(
            "Playwright subprocess creation failed. This is often caused by Anaconda's asyncio. "
            "Try using standard Python instead of Anaconda, or the site will be scraped using static HTML only."
        ) from e

