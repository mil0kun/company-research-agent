import re

def clean_title(title: str) -> str:
    """
    Clean and normalize a title by removing common patterns and noise.
    """
    if not title:
        return ""
    
    # Remove trailing indicators like " - Tavily Search"
    title = re.sub(r'\s*[-–|]\s*[^-–|]*$', '', title)
    
    # Remove common URL components
    title = re.sub(r'https?://(www\.)?', '', title)
    
    # Remove trailing domain-like patterns
    title = re.sub(r'\.[a-z]{2,4}(/.*)?$', '', title)
    
    # Remove excess whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title
