import httpx
from bs4 import BeautifulSoup
from app.util.url_util import validate_url, resolve_absolute_url
from app.util.noise_filter import remove_noise

async def scrape_static(url: str) -> str:
    """
    Use requests/httpx to extract meta + raw HTML
    """
    if not validate_url(url):
        raise ValueError(f"Invalid URL: {url}")
    
    # More realistic browser headers to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30.0) as client:
        try:
            response = await client.get(url)
            
            # Handle 403 Forbidden specifically
            if response.status_code == 403:
                raise ValueError(
                    f"HTTP 403 Forbidden: The website is blocking automated requests. "
                    f"This may be due to bot protection. Try a different URL or the site may require authentication."
                )
            
            response.raise_for_status()
            
            html_content = response.text
            
            # Remove noise (cookie banners, modals, etc.)
            html_content = remove_noise(html_content)
            
            return html_content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError(
                    f"HTTP 403 Forbidden: The website is blocking automated requests. "
                    f"URL: {url}"
                )
            raise ValueError(f"HTTP error {e.response.status_code}: {e.response.reason_phrase}")
        except httpx.HTTPError as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")

