"""
Simple script to test the API endpoints
Run this after starting the server to verify everything works
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/healthz")
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Server is not running!")
        print("Please start the server first with: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scrape():
    """Test the scrape endpoint"""
    try:
        test_url = "https://example.com"
        response = requests.post(
            f"{BASE_URL}/scrape",
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        print(f"\nScrape Test Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"URL: {data.get('url')}")
            print(f"Sections found: {len(data.get('sections', []))}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Lyftr AI Web Scraper API")
    print("=" * 50)
    
    health_ok = test_health()
    
    if health_ok:
        print("\n✅ Health endpoint is working!")
        test_scrape()
    else:
        print("\n❌ Health endpoint failed. Please check your server.")

