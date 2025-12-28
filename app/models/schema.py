from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional

class Section(BaseModel):
    label: str
    type: str
    content: str
    block: Dict[str, Any]
    truncated: bool
    rawHtml: str

class ScrapeResponse(BaseModel):
    url: str
    sections: List[Section]

