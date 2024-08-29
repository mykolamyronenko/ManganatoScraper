import logging
from scraper import MangaScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_scraping(urls, progress_callback=None):
    scraper = MangaScraper(urls, progress_callback)
    scraper.scrape()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manga Scraper")
    parser.add_argument('--url', type=str, help="URL of the manga to scrape")
    parser.add_argument('--file', type=str, help="File containing URLs of the manga to scrape")
    parser.add_argument('--gui', action='store_true', help="Run the application in GUI mode")
    args = parser.parse_args()

    if args.gui:
        from gui import run_gui
        run_gui()
    elif args.url:
        start_scraping(args.url)
    elif args.file:
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
        start_scraping(urls)
    else:
        print("Visit Manganato.com to get the manga link.")
        url = input("Enter the URL of the manga to scrape: ")
        start_scraping(url)

if __name__ == "__main__":
    main()
