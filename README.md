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
  - `customtkinter`
  - `CTkMessagebox`

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/manga-scraper.git
   cd manga-scraper
   ```

2. **Create a virtual environment:**
   ```
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
      ```
      .venv\Scripts\activate
      ```

   - On macOS/Linux:
      ```
      source .venv/bin/activate
      ```
   
4. **Activate the virtual environment:**
    ```  
    pip install -r requirements.txt
    ```

## Running the Application

   - CLI Mode: Run the application with a URL argument:
      ``` 
      python main.py --url https://manganato.com/manga-example  
      ```
   - CLI Mode with File: Run the application with a file containing URLs:
      ```  
      python main.py --file "links.txt"
      ```
   - GUI Mode: Run the application with the --gui flag:
      ```
      python main.py --gui
      ```



