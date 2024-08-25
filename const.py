import json

with open('headers.json', 'r') as f:
    config = json.load(f)

HEADERS = config['headers']
IMAGE_HEADERS = config['image_headers']
