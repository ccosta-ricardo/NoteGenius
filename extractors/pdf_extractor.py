from PyPDF2 import PdfReader

class PDFExtractor:
    def __init__(self, file_path, page_range=None):
        """
        Inicializa o extrator de PDF.
        page_range: tupla (início, fim) ou None para todas as páginas
        """
        self.file_path = file_path
        self.page_range = page_range
    
    def extract_text(self):
        """Extrai texto de um arquivo PDF."""
        reader = PdfReader(self.file_path)
        text = ""
        
        # Define o range de páginas
        start = self.page_range[0] - 1 if self.page_range else 0
        end = self.page_range[1] if self.page_range else len(reader.pages)
        
        # Valida o range
        if start < 0 or end > len(reader.pages) or start >= end:
            raise ValueError("Range de páginas inválido")
        
        # Extrai texto das páginas selecionadas
        for page_num in range(start, end):
            text += f"\n--- Página {page_num + 1} ---\n"
            text += reader.pages[page_num].extract_text()
        
        return text 