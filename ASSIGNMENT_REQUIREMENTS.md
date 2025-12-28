# Lyftr AI - Full-Stack Alignment Assignment Requirements

Based on the ChatGPT conversation analysis, here are the extracted assignment requirements:

## 📋 Mandatory Root Files

### 1. `run.sh`
- Create virtual environment
- Install dependencies
- Start server at http://localhost:8000

### 2. `requirements.txt`
Required dependencies:
- FastAPI / Flask
- httpx / requests
- BeautifulSoup / selectolax
- Playwright
- uvicorn

### 3. `README.md`
Must include:
- Setup + run instructions
- Test URLs (3 minimum)
- Limitations

### 4. `design_notes.md`
Must document:
- Static vs JS fallback strategy
- Playwright wait strategy
- Click & scroll logic
- Section grouping & truncation

### 5. `capabilities.json`
- Boolean flags of implemented features

## 🔧 Backend Requirements (`app/`)

### `main.py`
- FastAPI app initialization
- Include routers
- Serve frontend at `/`

### API Routes (`app/api/`)

#### `health.py` → GET `/healthz`
- Health check endpoint

#### `scrape.py` → POST `/scrape`
- Main scraping endpoint
- Accepts URL in request body
- Returns structured JSON response

## 🧠 Core Scraping Logic (`app/core/`)

### `static_scraper.py`
- Use requests/httpx
- Extract meta + raw HTML
- Fallback for simple static sites

### `js_scraper.py`
- Playwright rendering
- Scroll + click flow
- Handle JavaScript-heavy sites

### `heuristic.py`
- Decide when static HTML is insufficient
- Trigger JS fallback automatically
- Smart detection of JS-dependent content

### `interactions.py`
- Handle tabs
- Load more buttons
- Infinite scroll / pagination
- Dynamic content loading

### `section_parser.py`
- Convert HTML → section-aware JSON
- Generate structured output with:
  - `label`: Section heading/identifier
  - `type`: Section type (header, content, sidebar, etc.)
  - `content`: Text content
  - `block`: Block structure (lists, tables, images, links)
  - `truncated`: Boolean if content was truncated
  - `rawHtml`: Original HTML

## 📊 Models (`app/models/`)

### `schema.py`
- Pydantic models
- Ensure output JSON matches required schema exactly
- Request/Response validation

## 🛠️ Utilities (`app/util/`)

### `url_util.py`
- Absolute URL resolution
- URL validation (http/https only)

### `html_util.py`
- Text extraction
- List & table parsing

### `noise_filter.py`
- Remove cookie banners
- Remove modals / overlays
- Clean HTML content

## 🎨 Frontend Requirements

### Backend-rendered UI (Recommended)

#### `templates/index.html`
- Main HTML template

#### `static/frontend.js`
- Frontend JavaScript

### Required Features:
1. **URL input** - Input field for target URL
2. **Scrape button** - Trigger scraping action
3. **Loading state** - Show progress during scraping
4. **Section accordion** - Expandable sections display
5. **JSON viewer** - Display structured JSON output
6. **Download JSON button** - Export results as JSON file

## ✅ Evaluation Criteria

The structure should:
- Match all required endpoints
- Have clean separation of concerns
- Be easy to run via `./run.sh`
- Be simple to inspect manually
- Be friendly to automated tests
- Fully satisfy frontend evaluation stage

## 📝 Notes

- The assignment is based on "Lyftr AI — Full-Stack Alignment.pdf"
- The project structure should make evaluation easy
- All mandatory files must be present
- API endpoints must match exactly: `/healthz` and `/scrape`
- Output JSON must match the required schema

