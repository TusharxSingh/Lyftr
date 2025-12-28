from bs4 import BeautifulSoup
from typing import List, Dict, Any
from app.util.html_util import extract_text, parse_lists, parse_tables

def parse_sections(html_content: str) -> List[Dict[str, Any]]:
    """
    Convert HTML → section-aware JSON
    Generate: label, type, content, block, truncated, rawHtml
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = []
    
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Find main content areas
    main_content = soup.find('main') or soup.find('article') or soup.find('body')
    
    if not main_content:
        return sections
    
    # Group by semantic HTML elements
    section_elements = main_content.find_all(['section', 'article', 'div', 'header', 'footer', 'nav', 'aside'])
    
    for idx, element in enumerate(section_elements[:20]):  # Limit to 20 sections
        try:
            # Extract label (heading or id/class)
            label = extract_section_label(element)
            
            # Determine type
            section_type = determine_section_type(element)
            
            # Extract content
            content = extract_text(element)
            
            # Check if truncated (content too long)
            truncated = len(content) > 5000
            if truncated:
                content = content[:5000] + "..."
            
            # Get raw HTML
            try:
                raw_html = str(element)
            except Exception:
                raw_html = ""
            
            # Extract block structure
            block = extract_block_structure(element)
            
            sections.append({
                "label": label,
                "type": section_type,
                "content": content,
                "block": block,
                "truncated": truncated,
                "rawHtml": raw_html
            })
        except Exception as e:
            # Skip problematic elements and continue
            continue
    
    return sections

def extract_section_label(element) -> str:
    """Extract label from heading, id, or class"""
    # Try heading first - check each heading level
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        heading = element.find(tag)
        if heading:
            text = heading.get_text(strip=True)
            if text:
                return text
    
    # Try id
    if element.get('id'):
        return element.get('id')
    
    # Try class
    if element.get('class'):
        classes = element.get('class')
        if isinstance(classes, list):
            return ' '.join(classes)
        return str(classes)
    
    # Fallback to tag name
    tag_name = element.name if hasattr(element, 'name') else 'div'
    return f"Section {tag_name}"

def determine_section_type(element) -> str:
    """Determine section type based on element and content"""
    if not hasattr(element, 'name'):
        return 'section'
    
    tag_name = element.name.lower() if element.name else 'div'
    
    if tag_name in ['header', 'footer', 'nav']:
        return tag_name
    
    # Check for common patterns
    classes = element.get('class', [])
    if isinstance(classes, list):
        class_str = ' '.join(classes).lower()
    else:
        class_str = str(classes).lower()
    
    if 'hero' in class_str or 'banner' in class_str:
        return 'hero'
    if 'content' in class_str or 'main' in class_str:
        return 'content'
    if 'sidebar' in class_str or 'aside' in class_str:
        return 'sidebar'
    if 'footer' in class_str:
        return 'footer'
    if 'header' in class_str or 'nav' in class_str:
        return 'navigation'
    
    return 'section'

def extract_block_structure(element) -> Dict[str, Any]:
    """Extract block structure (lists, tables, etc.)"""
    block = {
        "lists": parse_lists(element),
        "tables": parse_tables(element),
        "images": len(element.find_all('img')),
        "links": len(element.find_all('a'))
    }
    return block

