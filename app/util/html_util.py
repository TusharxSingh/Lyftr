from bs4 import BeautifulSoup
from typing import List, Dict, Any

def extract_text(element) -> str:
    """Extract text content from HTML element"""
    return element.get_text(separator=' ', strip=True)

def parse_lists(element) -> List[Dict[str, Any]]:
    """Parse list & table parsing"""
    lists = []
    for ul in element.find_all(['ul', 'ol']):
        items = [li.get_text(strip=True) for li in ul.find_all('li')]
        lists.append({
            "type": ul.name,
            "items": items,
            "count": len(items)
        })
    return lists

def parse_tables(element) -> List[Dict[str, Any]]:
    """Parse tables from HTML"""
    tables = []
    for table in element.find_all('table'):
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            rows.append(cells)
        tables.append({
            "rows": rows,
            "row_count": len(rows),
            "col_count": len(rows[0]) if rows else 0
        })
    return tables

