# Troubleshooting Guide

## 500 Internal Server Error

If you're getting a 500 error when scraping, check the following:

### 1. Check Server Terminal
Look at the terminal where you're running `uvicorn`. You should see detailed error messages that will help identify the issue.

### 2. Common Issues Fixed:
- ✅ Fixed `find()` bug in section parser (was using list instead of individual tags)
- ✅ Added better error handling for None values
- ✅ Improved exception handling in interactions
- ✅ Added traceback logging for debugging

### 3. Test with Simple URL First
Try `https://example.com` - this should always work and helps verify the scraper is functioning.

### 4. Check Dependencies
Make sure all dependencies are installed:
```powershell
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 5. Restart Server
After code changes, restart the server:
```powershell
# Press Ctrl+C to stop, then:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Common Error Messages

### "Scraping failed: HTTP error 403"
- The website is blocking automated requests
- Try a different URL

### "Scraping failed: Request timeout"
- The website took too long to load
- Try a simpler/faster website

### "Scraping failed: Failed to navigate"
- The website may require authentication
- The URL might be invalid
- Network issues

### "No sections found"
- The scraper worked but couldn't find structured content
- This is normal for some websites
- Try a content-rich site like Wikipedia

