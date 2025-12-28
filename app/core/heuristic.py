import httpx
from bs4 import BeautifulSoup

async def should_use_js_scraper(url: str) -> bool:
    """
    Decide when static HTML is insufficient
    Trigger JS fallback
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)
            
            # If we get 403, don't try JS scraper (it will also fail)
            # Just return False to use static scraper which will handle the error
            if response.status_code == 403:
                return False
            
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check for indicators that JS is needed
            # 1. Check for script tags that modify content
            scripts = soup.find_all('script')
            has_react = any('react' in str(script).lower() or 'react-dom' in str(script).lower() for script in scripts)
            has_vue = any('vue' in str(script).lower() for script in scripts)
            has_angular = any('angular' in str(script).lower() for script in scripts)
            
            # 2. Check for noscript tags (indicates JS-dependent content)
            noscript = soup.find('noscript')
            has_noscript = noscript is not None
            
            # 3. Check for data attributes that suggest dynamic content
            has_data_attrs = bool(soup.find_all(attrs=lambda x: x and any(k.startswith('data-') for k in x.keys())))
            
            # 4. Check if content seems minimal (might be loaded by JS)
            body = soup.find('body')
            if body:
                text_content = body.get_text(strip=True)
                if len(text_content) < 500:  # Very little content suggests JS loading
                    return True
            
            # Use JS scraper if framework detected or other indicators
            return has_react or has_vue or has_angular or (has_noscript and has_data_attrs)
            
    except Exception:
        # If static scraping fails, try JS
        return True

