from playwright.async_api import Page
import asyncio

async def handle_interactions(page: Page):
    """
    Handle: Tab, Load more, Infinite scroll / pagination
    """
    try:
        # Wait for initial load
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        # If networkidle times out, continue anyway
        pass
    
    # Handle infinite scroll
    try:
        await handle_infinite_scroll(page)
    except Exception:
        pass
    
    # Handle "Load more" buttons
    try:
        await handle_load_more_buttons(page)
    except Exception:
        pass
    
    # Handle tabs
    try:
        await handle_tabs(page)
    except Exception:
        pass
    
    # Final wait for any remaining content
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass

async def handle_infinite_scroll(page: Page, max_scrolls: int = 5):
    """Handle infinite scroll by scrolling down multiple times"""
    last_height = await page.evaluate("document.body.scrollHeight")
    
    for _ in range(max_scrolls):
        # Scroll to bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Wait for new content
        await asyncio.sleep(2)
        
        # Check if new content loaded
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

async def handle_load_more_buttons(page: Page):
    """Click 'Load more' buttons if present"""
    load_more_selectors = [
        'button:has-text("Load more")',
        'button:has-text("Show more")',
        'a:has-text("Load more")',
        '[class*="load-more"]',
        '[id*="load-more"]'
    ]
    
    for selector in load_more_selectors:
        try:
            button = page.locator(selector).first
            if await button.is_visible():
                await button.click()
                await page.wait_for_load_state("networkidle", timeout=5000)
                await asyncio.sleep(1)
        except Exception:
            continue

async def handle_tabs(page: Page):
    """Handle tab navigation if present"""
    tab_selectors = [
        '[role="tab"]',
        '.tab',
        '[class*="tab"]'
    ]
    
    for selector in tab_selectors:
        try:
            tabs = await page.locator(selector).all()
            for tab in tabs[:3]:  # Limit to first 3 tabs
                if await tab.is_visible():
                    await tab.click()
                    await page.wait_for_load_state("networkidle", timeout=5000)
                    await asyncio.sleep(1)
        except Exception:
            continue

