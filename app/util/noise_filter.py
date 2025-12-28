from bs4 import BeautifulSoup

def remove_noise(html_content: str) -> str:
    """
    Remove cookie banner
    Remove modals / overlay
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove cookie banners
    cookie_selectors = [
        '[id*="cookie"]',
        '[class*="cookie"]',
        '[id*="consent"]',
        '[class*="consent"]',
        '[id*="gdpr"]',
        '[class*="gdpr"]'
    ]
    
    for selector in cookie_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    # Remove modals and overlays
    modal_selectors = [
        '[class*="modal"]',
        '[id*="modal"]',
        '[class*="overlay"]',
        '[id*="overlay"]',
        '[class*="popup"]',
        '[id*="popup"]',
        '[role="dialog"]'
    ]
    
    for selector in modal_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    # Remove script and style tags
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    return str(soup)

