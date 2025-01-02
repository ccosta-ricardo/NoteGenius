from PyPDF2 import PdfReader

class PDFExtractor:
    def __init__(self, file_path, page_range=None):
        """
        Initializes the PDF extractor.
        page_range: tuple (start, end) or None for all pages
        """
        self.file_path = file_path
        self.page_range = page_range
    
    def extract_text(self):
        """Extracts text from a PDF file."""
        reader = PdfReader(self.file_path)
        text = ""
        
        # Define page range
        start = self.page_range[0] - 1 if self.page_range else 0
        end = self.page_range[1] if self.page_range else len(reader.pages)
        
        # Validate range
        if start < 0 or end > len(reader.pages) or start >= end:
            raise ValueError("Invalid page range")
        
        # Extract text from selected pages
        for page_num in range(start, end):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += reader.pages[page_num].extract_text()
        
        return text 