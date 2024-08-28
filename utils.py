import os
import logging
from PIL import Image
from tqdm import tqdm
import re
import requests

def create_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
    except OSError as e:
        logging.error(f"Error creating folder {folder_name}: {e}")

def convert_images_to_pdf(image_folder, pdf_path):
    images = []
    image_files = sorted(os.listdir(image_folder), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    for file_name in image_files:
        if file_name.endswith(('.webp', '.jpg', '.png')):
            image_path = os.path.join(image_folder, file_name)
            image = Image.open(image_path).convert('RGB')
            images.append(image)
    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        logging.info(f'Created PDF: {pdf_path}')

def folder_contains_images_and_pdf(folder_name):
    if not os.path.exists(folder_name):
        return False
    images_exist = any(file_name.endswith(('.webp', '.jpg', '.png')) for file_name in os.listdir(folder_name))
    pdf_exists = any(file_name.endswith('.pdf') for file_name in os.listdir(folder_name))
    return images_exist and pdf_exists

def download_with_progress(url, headers, file_path):
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    with open(file_path, 'wb') as file, tqdm(
        desc=file_path,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
