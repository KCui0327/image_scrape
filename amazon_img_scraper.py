import requests
import re
from bs4 import BeautifulSoup
import urllib
from datetime import datetime
import main
import xlsxwriter

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
    'Accept-Language': 'en-US, en;q=0.5'
}
def amazon_image_scrape(name_item):
    workbook = xlsxwriter.Workbook("image_data_amazon.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write("A1", "Title")
    worksheet.write("B1", "URL")
    worksheet.write("C1", "Time")
    worksheet.write("D1", "Source")

    row = 1

    search_url = "https://www.amazon.com/s?k={topic}&ref=nb_sb_noss_2"
    search_url.format(topic=name_item)

    html = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(html.content, features="lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    arr_list = []

    for link in links:
        arr_list.append(link.get('href'))

    for link in arr_list:
        webpage_url = "https://www.amazon.com" + link
        webpage = requests.get(webpage_url, headers=HEADERS)
        new_soup = BeautifulSoup(webpage.content, "lxml")

        # get product title
        try:
            title = new_soup.find("span", attrs={"id": 'productTitle'}).text.strip()
        except AttributeError:
            print("Cannot retrieve product title")

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        img_data_elem = main.ImageData(title, webpage_url, formatted_time, "Amazon")
        worksheet.write(row, 0, img_data_elem.img_title)
        worksheet.write(row, 1, img_data_elem.source)
        worksheet.write(row, 2, img_data_elem.time_scraped)
        worksheet.write(row, 3, img_data_elem.source)
        row += 1

        images = re.findall('"hiRes":"(.+?)"', webpage.text)

        for num, img_url in enumerate(images):
            img_filename = "./img/{topic}/image{i}_amazon.jpg"
            img_filename.format(topic=name_item, i=num)
            urllib.request.urlretrieve(img_url, img_filename)