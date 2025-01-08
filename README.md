# NoteGenius

A desktop application that automates content extraction and summarization for Obsidian notes. Using AI, it processes PDFs, YouTube videos, websites, and manual input to generate well-structured markdown notes.

## Features
- Multiple input sources:
  - PDF files with page range selection
  - YouTube videos (automatic transcription)
  - Websites (article extraction)
  - Manual input for direct AI processing
- Customizable layouts for different content types:
  - Video summaries
  - Book chapters
  - Articles
  - Technical documentation (MIAD)
- Multi-language support:
  - English
  - Portuguese (European)
  - Spanish
- Direct integration with Obsidian vault
- Caching system for YouTube transcriptions
- Modern and clean interface

## Prerequisites
- Python 3.10 or higher
- FFmpeg (required for YouTube audio processing)
- Google API Key for Gemini AI
- Obsidian installed (optional, but recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ccosta-ricardo/NoteGenius.git
cd NoteGenius
```

2. Create and activate a virtual environment:

**Windows:** 
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:** 
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey:
  ```bash
  choco install ffmpeg
  ```
- Linux:
  ```bash
  sudo apt install ffmpeg
  ```
- Mac:
  ```bash
  brew install ffmpeg
  ```

## Configuration

1. Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

2. Create `config.py` based on `config_example.py`:
- Set `OUTPUT_DIR` to your Obsidian vault path or desired output directory
- Customize layouts and prompts if needed
- Adjust interface settings if desired

## Usage

1. Run the application:
```bash
python main.py
```

2. Select input type:
- PDF File: Choose a PDF and optionally specify page range
- YouTube Link: Paste a YouTube URL
- Website URL: Paste any article URL
- Manual Input: Direct AI processing without source content

3. Enter filename for the markdown file or choose an existing file.

4. (Optional) Add specific instructions for the AI

5. Select language and layout

6. Click "Generate Summary"

## Project Structure
```
NoteGenius/
├── main.py              # Application entry point
├── interface.py         # GUI implementation
├── processor.py         # Content processing logic
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── extractors/         # Content extractors
│   ├── pdf_extractor.py
│   ├── youtube_extractor.py
│   └── url_extractor.py
└── theme/             # UI theme configuration
    └── theme_generator.py
```

## Troubleshooting

1. FFmpeg not found:
- Ensure FFmpeg is installed and accessible from command line
- Try reinstalling FFmpeg

2. API Key errors:
- Verify `.env` file exists and contains valid API key
- Check if environment variables are loading correctly

3. YouTube processing issues:
- Check internet connection
- Verify video is accessible
- Clear cache directory if needed

