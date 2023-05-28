import os
import parse_list as data
import google_img_scraper as gg
import amazon_img_scraper as az

parent_path = "./img"

for name in data.arr_item_name:
    img_item_path = os.path.join(parent_path, name)
    os.makedirs(img_item_path, exist_ok=True)

class ImageData:
    img_title: str
    img_url: str
    time_scraped: float
    source: str

for name in data.arr_item_name:
    gg.google_image_scrape(name)
    az.amazon_image_scrape(name)