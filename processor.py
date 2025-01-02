"""
Core processing engine for NoteGenius.
Manages the entire content processing pipeline:
1. Content extraction using appropriate extractors
2. AI processing using Gemini API
3. Markdown file generation and saving

The processor coordinates between:
- Different content extractors (PDF, YouTube, URL)
- AI model for summary generation
- File system for saving outputs
"""

import os
from pathlib import Path
from extractors.pdf_extractor import PDFExtractor
from extractors.youtube_extractor import YouTubeExtractor
from extractors.url_extractor import URLExtractor
import google.generativeai as genai
from dotenv import load_dotenv
from config import LLM_MODEL, OUTPUT_DIR, LAYOUTS, BASE_PROMPT

class ContentProcessor:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Configure Gemini
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(LLM_MODEL)
    
    def process_content(self, input_type, input_value, output_filename, layout, language, instructions, page_range=None):
        """Processes content based on input type."""
        try:
            # 1. Extract content
            content = self._extract_content(input_type, input_value, page_range)
            
            # 2. Generate summary using AI
            summary = self._generate_summary(content, layout, language, instructions)
            
            # 3. Save file
            self._save_output(summary, output_filename)
            
            return True, "Processing completed successfully!"
            
        except Exception as e:
            return False, f"Error during processing: {str(e)}"
    
    def _extract_content(self, input_type, input_value, page_range=None):
        """Extracts content based on input type."""
        if input_type == "Manual Input":
            return None  # Returns None to indicate no content to extract
        
        elif input_type == "file":
            extractor = PDFExtractor(input_value, page_range)
            return extractor.extract_text()
        
        elif input_type == "youtube":
            extractor = YouTubeExtractor(input_value)
            return extractor.transcribe()
        
        elif input_type == "url":
            extractor = URLExtractor(input_value)
            return extractor.extract_content()
        
        else:
            raise ValueError(f"Invalid input type: {input_type}")
    
    def _generate_summary(self, content, layout, language, instructions):
        """Generates summary using AI."""
        layout_info = LAYOUTS.get(layout)
        if not layout_info:
            raise ValueError(f"Invalid layout: {layout}")
        
        # Prepare prompt parts
        if content:
            prefix = f"Analyze the following content and generate a structured summary in {language}."
            content_section = f"Content:\n{content}"
        else:
            prefix = f"Generate a structured summary in {language} based on the instructions below."
            content_section = ""
        
        prompt = BASE_PROMPT.format(
            prefix=prefix,
            language=language,
            layout_prompt=layout_info["prompt"],
            instructions=instructions,
            content_section=content_section
        )
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7
                )
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error processing AI response: {str(e)}")
    
    def _save_output(self, content, filename):
        """Saves processed content to a markdown file."""
        # Ensure directory exists
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Add .md extension if not present
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Use complete Obsidian path
        output_path = OUTPUT_DIR / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Error saving file to Obsidian: {str(e)}") 