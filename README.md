# Lyftr AI - Web Scraper

A full-stack web scraping application that extracts structured content from websites using both static HTML parsing and JavaScript rendering.

## Setup + Run Instructions

### For Linux/Mac:

1. Make run.sh executable:
   ```bash
   chmod +x run.sh
   ```

2. Run the setup script:
   ```bash
   ./run.sh
   ```

### For Windows:

1. Run the batch file:
   ```cmd
   run.bat
   ```

   Or manually:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   python start_server.py
   ```

   **Important for Anaconda users:** If you're using Anaconda Python and get `NotImplementedError` with Playwright, use `start_server.py` instead of running uvicorn directly. This script fixes the asyncio event loop policy issue.

3. The server will start at http://localhost:8000

4. Open your browser and navigate to http://localhost:8000

## API Endpoints

- `GET /healthz` - Health check endpoint
- `POST /scrape` - Main scraping endpoint
  - Request body: `{"url": "https://example.com"}`
  - Returns: Structured JSON with sections

## Test URLs (3 minimum)

1. **Simple Static Site**: https://example.com
   - Good for testing static HTML scraping
   - ✅ Should work reliably

2. **HTTPBin Test Site**: https://httpbin.org/html
   - Simple HTML page for testing
   - ✅ Should work reliably

3. **News/Content Site**: https://news.ycombinator.com
   - Tests section parsing and content extraction
   - ✅ Should work reliably

### URLs that may not work:
- **Wikipedia** - Often blocks automated requests (403 Forbidden)
- Sites requiring authentication (Google Meet, Gmail, etc.)
- Sites with heavy bot protection (Cloudflare, etc.)
- Sites that block automated access
- Private/internal URLs

### If you get 403 Forbidden:
Some websites (like Wikipedia) actively block automated scrapers. This is normal and expected. Try:
- `https://example.com` - Always works
- `https://httpbin.org/html` - Test site that allows scraping
- `https://quotes.toscrape.com/` - Scraping practice site

## Features

- ✅ Static HTML scraping (httpx)
- ✅ JavaScript rendering (Playwright)
- ✅ Automatic JS fallback detection
- ✅ Section-aware parsing
- ✅ Noise filtering (removes banners, modals)
- ✅ Interactive element handling (scroll, click, tabs)
- ✅ Structured JSON output
- ✅ Web UI for testing

## Limitations

- Playwright requires browser installation (handled automatically in setup)
- Some sites may block automated requests
- Very large pages may take time to process
- Dynamic content that loads after long delays may not be captured
- Rate limiting not implemented (be respectful when scraping)
- Some sites may require authentication (not supported)

