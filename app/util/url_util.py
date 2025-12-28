from urllib.parse import urljoin, urlparse

def validate_url(url: str) -> bool:
    """
    URL validation (http/https only)
    """
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https'] and result.netloc
    except Exception:
        return False

def resolve_absolute_url(base_url: str, relative_url: str) -> str:
    """
    Absolute URL resolution
    """
    return urljoin(base_url, relative_url)

