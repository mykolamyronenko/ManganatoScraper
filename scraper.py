import requests
from lxml import html
import logging
import os
import shutil
from const import HEADERS, IMAGE_HEADERS
from utils import create_folder, convert_images_to_pdf, folder_contains_images_and_pdf, download_with_progress

class MangaScraper:
    def __init__(self, urls, progress_callback=None):
        self.urls = urls if isinstance(urls, list) else [urls]
        self.headers = HEADERS
        self.image_headers = IMAGE_HEADERS
        self.progress_callback = progress_callback

    def fetch_page_content(self, url):
        try:
            response = requests.get(url, headers=self.headers)
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
                if img_url and img_url.endswith(('.webp', '.jpg', '.png')):
                    img_name = os.path.join(chapter_folder, os.path.basename(img_url))
                    download_with_progress(img_url, self.image_headers, img_name)
                    logging.info(f'Downloaded {img_name}')
        except requests.RequestException as e:
            logging.error(f"Error downloading images: {e}")

    def scrape(self):
        manga_folder = "Manga"
        create_folder(manga_folder)

        for url in self.urls:
            tree = self.fetch_page_content(url)
            if tree is None:
                logging.error("Failed to fetch the webpage content.")
                continue

            manga_name = tree.xpath('//h1/text()')[0]
            manga_path = os.path.join(manga_folder, manga_name)
            logging.info(f'Creating folder: {manga_path}')
            create_folder(manga_path)

            chapters = self.get_chapters(tree)
            logging.info(f'Found {len(chapters)} chapters.')

            pdf_folder = os.path.join(manga_path, "Pdf Chapters")
            create_folder(pdf_folder)

            for i, chapter in enumerate(chapters):
                link = chapter.get('href')
                logging.info(f'Processing chapter: {link}')
                chapter_name = chapter.text_content().strip()
                if ':' in chapter_name:
                    chapter_name = chapter_name.split(':')[0].strip()
                chapter_folder = os.path.join(manga_path, chapter_name)
                
                if folder_contains_images_and_pdf(chapter_folder):
                    logging.info(f'Skipping chapter {chapter_name} as it already contains images and a PDF.')
                    continue

                create_folder(chapter_folder)
                self.download_images(link, chapter_folder)
                pdf_path = os.path.join(chapter_folder, f"{chapter_name}.pdf")
                convert_images_to_pdf(chapter_folder, pdf_path)

                # Copy the PDF to the new folder
                shutil.copy(pdf_path, pdf_folder)

                # Update progress
                if self.progress_callback:
                    self.progress_callback(i + 1, len(chapters))

        logging.info('Done')
