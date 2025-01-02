import requests
from bs4 import BeautifulSoup
import trafilatura

"""
Website content extractor for NoteGenius.
Features:
- Article extraction using trafilatura
- Fallback to BeautifulSoup for complex pages
- Clean content parsing (removes ads, navigation, etc.)
- Title and main content separation
"""

class URLExtractor:
    def __init__(self, url):
        self.url = url
    
    def extract_content(self):
        """Extracts content from a URL."""
        try:
            # First try with trafilatura for better article extraction
            downloaded = trafilatura.fetch_url(self.url)
            if downloaded:
                content = trafilatura.extract(downloaded)
                if content:
                    return content
            
            # Fallback to BeautifulSoup if trafilatura fails
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extract title
            title = soup.find('title').text if soup.find('title') else ''
            
            # Extract main content
            article = soup.find('article') or soup.find('main') or soup.find('body')
            content = article.get_text(separator='\n', strip=True)
            
            return {
                'title': title,
                'content': content
            }
            
        except Exception as e:
            raise Exception(f"Error extracting content from URL: {str(e)}") 