import requests
from bs4 import BeautifulSoup
import trafilatura

class URLExtractor:
    def __init__(self, url):
        self.url = url
    
    def extract_content(self):
        """Extrai conteúdo de uma URL."""
        try:
            # Tenta primeiro com trafilatura para melhor extração de artigos
            downloaded = trafilatura.fetch_url(self.url)
            if downloaded:
                content = trafilatura.extract(downloaded)
                if content:
                    return content
            
            # Fallback para BeautifulSoup se trafilatura falhar
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove elementos indesejados
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extrai título
            title = soup.find('title').text if soup.find('title') else ''
            
            # Extrai conteúdo principal
            article = soup.find('article') or soup.find('main') or soup.find('body')
            content = article.get_text(separator='\n', strip=True)
            
            return {
                'title': title,
                'content': content
            }
            
        except Exception as e:
            raise Exception(f"Erro ao extrair conteúdo da URL: {str(e)}") 