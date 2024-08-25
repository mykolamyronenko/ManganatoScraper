# Manga Scraper

This project is a web scraper designed to download manga from a manganato.com and convert the images into PDF files.

## Features

- Fetches webpage content and extracts manga chapters.
- Downloads images from each chapter.
- Converts downloaded images into a PDF file.

## Requirements

- Python 3.6+
- The following Python libraries:
  - `requests`
  - `lxml`
  - `Pillow`
  - `tqdm`

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/manga-scraper.git
   cd manga-scraper

2. **Create a virtual environment:**
   python -m venv .venv

3. **Activate the virtual environment:**
    - On Windows:
      -`.venv\Scripts\activate`
    - On macOS/Linux:
      -`source .venv/bin/activate`
   
4. **Activate the virtual environment:**  
    - `pip install -r requirements.txt`
