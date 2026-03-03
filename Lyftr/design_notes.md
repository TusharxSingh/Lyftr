# Design Notes

## Static vs JS Fallback Strategy

- First attempt: Use static HTML scraper (requests/httpx)
- Fallback: If static HTML is insufficient, use Playwright for JS rendering
- Heuristic determines when to trigger JS fallback

## Playwright Wait Strategy

- Wait for network idle
- Wait for specific selectors
- Timeout handling

## Click & Scroll Logic

- Handle "Load more" buttons
- Infinite scroll detection
- Tab navigation
- Pagination support

## Section Grouping & Truncation

- Group content into logical sections
- Truncate long content appropriately
- Preserve structure and hierarchy

