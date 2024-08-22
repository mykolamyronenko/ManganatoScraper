import requests
from lxml import html
import logging
import os
from const import HEADERS, IMAGE_HEADERS
from utils import create_folder, convert_images_to_pdf, folder_contains_images_and_pdf, download_with_progress

class MangaScraper:
    def __init__(self, url):
        self.url = url
        self.headers = HEADERS
        self.image_headers = IMAGE_HEADERS

    def fetch_page_content(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return html.fromstring(response.content)
        except requests.RequestException as e:
            logging.error(f"Error fetching page content: {e}")
            return None

    def get_chapters(self, tree):
        return tree.xpath('//a[@class="chapter-name text-nowrap"]')

    def download_images(self, chapter_url, chapter_folder):
        try:
            image_response = requests.get(chapter_url, headers=self.headers)
            image_response.raise_for_status()
            img_tree = html.fromstring(image_response.content)
            images = img_tree.xpath('//div[@class="container-chapter-reader"]//img')
            for img in images:
                img_url = img.get('src')
                if img_url.endswith(('.webp', '.jpg', '.png')):
                    img_name = os.path.join(chapter_folder, os.path.basename(img_url))
                    download_with_progress(img_url, self.image_headers, img_name)
                    logging.info(f'Downloaded {img_name}')
        except requests.RequestException as e:
            logging.error(f"Error downloading images: {e}")

    def scrape(self):
        tree = self.fetch_page_content()
        if tree is None:
            logging.error("Failed to fetch the webpage content.")
            return

        folder = tree.xpath('//h1/text()')[0]
        logging.info(f'Creating folder: {folder}')
        create_folder(folder)
        chapters = self.get_chapters(tree)
        logging.info(f'Found {len(chapters)} chapters.')

        for chapter in chapters:
            link = chapter.get('href')
            logging.info(f'Processing chapter: {link}')
            chapter_name = chapter.text_content().strip()
            if ':' in chapter_name:
                chapter_name = chapter_name.split(':')[0].strip()
            chapter_folder = os.path.join(folder, chapter_name)
            
            if folder_contains_images_and_pdf(chapter_folder):
                logging.info(f'Skipping chapter {chapter_name} as it already contains images and a PDF.')
                continue

            create_folder(chapter_folder)
            self.download_images(link, chapter_folder)
            pdf_path = os.path.join(chapter_folder, f"{chapter_name}.pdf")
            convert_images_to_pdf(chapter_folder, pdf_path)

        logging.info('Done')
