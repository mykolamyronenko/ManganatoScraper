import logging
from scraper import MangaScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    url = input("Enter the URL of the webpage to scrape: ")
    scraper = MangaScraper(url)
    scraper.scrape()

if __name__ == "__main__":
    main()
